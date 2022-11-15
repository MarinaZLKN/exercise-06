import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from . import models
from . import serializers

connect_message = 'Connected!'
disconnect_message = 'Disconnected!'


class ChatConsumerAsyncWithChannelLayer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.group_name = None
        self.room_pk = None
        self.user = None

        super(ChatConsumerAsyncWithChannelLayer, self).__init__(*args, **kwargs)

    async def connect(self):
        room_pk = self.scope['url_route']['kwargs']['pk']
        user = self.scope['user']

        group_name = "room_%s" % room_pk

        self.group_name = group_name
        self.room_pk = room_pk
        self.user = user

        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )

        await self.accept()

        # This will send the static message to the chat on connection
        await self.send(text_data=json.dumps({
            'message': connect_message
        }))

    @sync_to_async
    def __room_message_persist(self, text_data):
        # Here we are going to save the message
        # Because every message belongs to a specific room, we have to access the existing room first
        # If the user was properly initialized in connect(self) and if the room exists
        if self.user is not None and models.Room.objects.filter(pk=self.room_pk).exists():
            room_model = models.Room.objects.get(pk=self.room_pk)
            text_data_json = json.loads(text_data)
            message_text = text_data_json['message']

            message_model = models.Message(
                room=room_model,
                text=message_text,
                user=self.user
            )
            message_model.save()
            print('message model saved', message_model)

            return message_model

        else:
            return None

    # Receive message from WebSocket (javascript on our web page)
    # This is forwarded to group
    # Then handled in chat_message(self, event)
    async def receive(self, text_data):
        message_model = await self.__room_message_persist(text_data=text_data)

        # If we successfully persisted (saved to database) the message
        # in our private method __room_message_persist(text_data)
        if message_model is not None:
            # We are going to serialize the message and send it back to our web page through the socket
            message_serialized = serializers.MessageSerializer(message_model).data

            await self.channel_layer.group_send(
                self.group_name,  # here we are accessing variable set in connect method
                {
                    'type': 'chat_message',
                    'message': message_serialized
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket (back to our web page, everyone who is inside the room will see it)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, message):
        await self.channel_layer.group_discard(
            self.group_name,  # here we are accessing variable set in connect method
            self.channel_name
        )
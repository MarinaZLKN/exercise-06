import json

from channels.generic.websocket import AsyncWebsocketConsumer

connect_message = 'Connected!'
disconnect_message = 'Disconnected!'


class ChatConsumerAsyncWithChannelLayer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "room_%s" % 1

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # This will send the static message to the chat on connection
        await self.send(text_data=json.dumps({
            'message': connect_message
        }))

    # Receive message from WebSocket (javascript on our web page)
    # This is forwarded to group
    # Then handled in chat_message(self, event)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_name,  # here we are accessing variable set in connect method
            {
                'type': 'chat_message',
                'message': message
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
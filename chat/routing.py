from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:pk>', consumers.ChatConsumerAsyncWithChannelLayer.as_asgi()),
]
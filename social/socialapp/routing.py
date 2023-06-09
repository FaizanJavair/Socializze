from django.urls import re_path

from . import consumers

# NOTE USE OF ws/ to separate out our ws URIs, like rest use of api/
# Websocket url pattern for the chat room
websocket_urlpatterns = [
    re_path(r'ws/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]

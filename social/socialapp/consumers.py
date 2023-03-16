import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Chat room functions to enable async communication
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # gets the user name as well
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group along with the user name
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group along with user who sent it
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket along with the user who sent it
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

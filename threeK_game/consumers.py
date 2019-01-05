from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

queue = []

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope['user']
        self.game_group_name = 'game_1'

        print(self.game_name)

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({
            'message': "polaczono ;)"
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )
    def game_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
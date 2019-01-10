from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .game import *
import json

queue = []

class GameConsumer(WebsocketConsumer):

    def update(self, arg):
        # tu trza connect to grupa konkretna z param from Match in Game
        self._match_start = arg
        self.game_group_name = 'game_' + str(arg)

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )
        self.is_in_group = True

    def connect(self):
        self.is_in_group = False
        self._match = None
        self._match_start = False
        self.accept()
        
        self.game_manager = GameManager()
        user = self.scope['user']
        self.game_manager.connect_player(self)
        print(self.game_manager.queue.print_content())

        self.send(text_data=json.dumps({
            'type': 'connect',
            'message': "connected successfully"
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

    def group_message(self, text):

        if self.is_in_group == False:
            print("Nie jestes w grupie")
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'game_message',
                    'message': text
                }
            )
    def notify_about_start(self, match_id):
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'create_match_message',
                'message': match_id
            }
        )

    def create_match_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'created_game',
            'match_id': message
        }))

    def game_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
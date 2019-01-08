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
        #self.group_message("elo w grupie")


    def connect(self):
        self.is_in_group = False
        self._match = None
        self._match_start = False
        self.accept()

        self.send(text_data=json.dumps({
            'message': "polaczono ;)"
        }))

        self.game_manager = GameManager()
        user = self.scope['user']
        self.game_manager.connect_player(self)
        print(self.game_manager.queue.print_content())
        # self.game_name = self.scope['user']
        # self.game_group_name = 'game_1'

        # print(self.game_name)

        # async_to_sync(self.channel_layer.group_add)(
        #     self.game_group_name,
        #     self.channel_name
        # )



    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


    def group_message(self, text):

        if self.is_in_group == False:
            print("Nie jestes w grupie")
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'game_message',
                    'message': text,
                }
            )

    def game_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .game import *
import json

queue = []
# Klasa Websocketu łącząca użytkowników w grupy do komunikacji w grze
class GameConsumer(WebsocketConsumer):

    # tworzy konkretna grupe( wywoływana z serwera)
    def update(self, arg):
        self._match_start = arg
        self.game_group_name = 'game_' + str(arg)
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )
        self.is_in_group = True

    # Podczas połączenia gracz jest łaczony z kolejką
    def connect(self):
        self.is_in_group = False
        self._match = None
        self._match_start = False
        self.accept()
        
        self.send(text_data=json.dumps({
            'content_type': 'connect',
            'message': "connected successfully"
        }))

        self.game_manager = GameManager()
        self.game_manager.connect_player(self)

    # podczas dc informowana jast gra o zdarzeniu
    def disconnect(self, close_code):
        if self._match != None:
            if self._match.is_end_match != True:
                # user dc during game
                self._match.disconnect(self)
        else:
            #user dc during queue
            pass

    #przekazanie wiadomości do serwera
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        x = text_data_json['x']
        y = text_data_json['y']

        if self._match != None:
            self._match.receive_message(text_data, self)

    # wysłanie wiadomośco grupowej
    def group_message(self, text, content_type):

        if self.is_in_group == False:
            print("Nie jestes w grupie")
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'game_message',
                    'content_type': content_type,
                    'message': text,
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
        content_type = event['content_type']

        self.send(text_data=json.dumps({
            'message': message,
            'content_type': content_type,
        }))
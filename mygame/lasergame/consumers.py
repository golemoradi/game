from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from channels.auth import get_user, logout
from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render

from lobby.views import new_game, join_game


class GameConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.game_id = 'lobby'
        super().__init__(*args, **kwargs)
        self.game_group_name = 'game_%s' % self.game_id
        self.user = self.scope['user']

        # self.room_name = self.scope['url_route']['kwargs']['room_name']

    def connect(self):
        self.game_id = 'lobby'
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.game_group_name = 'game_%s' % self.game_id
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        user = self.scope['user']
        if user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                user.username,
                self.channel_name
            )

        return self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # if (text_data_json['message']):
        #     message = text_data_json['message']
        #     user = self.scope['user']
        #
        #     if user.is_authenticated:
        #         message = user.username + ': ' + message
        #     else:
        #         message = 'Anonymous: ' + message
        #
        #     # Send message to room group
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.game_group_name,
        #         {
        #             'type': 'chat_message',
        #             'message': message
        #         }
        # )

        if (text_data_json.__contains__('action')):
            #return render(request, 'lobby.html', {})
            action = text_data_json['action']
            if (action =='create-game'):
                return new_game(self)

        if (text_data_json.__contains__('gameID')):
            #return render(request, 'lobby.html', {})
            gameID = text_data_json['gameID']
            return join_game(self, gameID)



        if (text_data_json['move']):
            move = text_data_json['move']
            player = text_data_json['player']
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'player': player,
                    'move': move
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

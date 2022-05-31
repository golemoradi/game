from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
#     """ "http": ,
#     "websocket": some_other_app, """
#     <str:room_name>
    #route('ws/lobby/', connect, name='chatroom'),
    path('ws/lobby/', consumers.GameConsumer, name='game'),
]
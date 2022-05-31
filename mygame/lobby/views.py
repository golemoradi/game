from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import logout
from django.core.serializers import json
from django.http import HttpResponseRedirect
from django.urls import reverse

from lobby.models import LobbyGames
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def new_game(request):
    if request.user.is_authenticated:
        game = LobbyGames()
        game.owner = request.user
        game.save()
        ID = game.owner.get_username
        return request.send(text_data=json.dumps({
            'gameID': ID
        }))
        # return render(request, 'lobby/lobby.html', {
        #     'gameID': ID
        #     # 'game': game
        # })



def join_game(request, owner):
    #text_data_json = json.loads(text_data)
    #owner = text_data_json['owner']

    try:
        LobbyGames.objects.get(owner=owner)
    except:
        print("An exception occurred")
    game = LobbyGames.objects.get(owner=owner)
    game.second_player = request.get_user
    game.save()
    # request.send(text_data=json.dumps({
    #     'gameID': owner
    # }))

def start_game(request):
    return render(request, 'game.html', {})

# record = MyModelName(my_field_name="Instance #1")
#
# # Save the object into the database.
# record.save()

# def index(request):
#     return render(request, 'chat/index.html', {})
#
#
# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name
#     })

def do_logout(request):
    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})

    logout(request)
    #return HttpResponseRedirect(reverse('login'))
    return render(request, 'welcome/index.html', {})
# Create your views here.

import self as self
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from . import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, path


def index(request):
    return render(request, 'welcome/index.html', {})


@login_required(login_url='/')
def info(request):
    return HttpResponseRedirect(reverse('lobby'))
    # return render(request, 'lobby/lobby.html', {})

    # return HttpResponse.__init__(content=b'', content_type=None, status=200, reason=None, charset=None)
    # return render(request, 'lobby/lobby.html', {})
    # return HttpResponse('Hello ' + request.user.username)
    # return path('lobby.html')


@login_required(login_url='/')
def lobby(request):
    return render(request, 'lobby/lobby.html', {})


def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'])
                # return HttpResponseRedirect(info)
                # return HttpResponse(template.render(context, request))
                return HttpResponseRedirect(reverse('index'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form
    return render(request, 'registration/signup.html', context)


def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                # return HttpResponseRedirect(reverse('info'))
                return info(request)
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    # return HttpResponseRedirect(reverse('lobby'))

    return render(request, 'registration/login.html', context)


def do_logout(request):
    if request.user.is_authenticated:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {
            'type': 'logout_message',
            'message': 'Disconnecting. You logged out from another browser or tab.'})

    logout(request)
    return HttpResponseRedirect(reverse('login'))

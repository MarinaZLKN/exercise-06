from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from chat import forms, models


def index(request):
    user = request.user
    if user.is_authenticated:
        room_list = models.Room.objects.filter(users__pk=user.pk).order_by('-updated')
        user_list = User.objects.exclude(pk=request.user.pk)
        return render(request, 'chat/index.html', {
            'room_list': room_list,
            'user_list': user_list
        })
    else:
        return redirect('chat:login_view')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('chat:index')
        else:
            return render(request, 'chat/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'chat/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:index')
        else:
            return render(request, 'chat/register.html', {'form': form})
    else:
        return render(request, 'chat/register.html', {'form': UserCreationForm()})


def log_out(request):
    logout(request)

    return redirect('chat:login_view')


def room_view(request, pk):
    return render(request, 'chat/room.html')


def room_add(request):
    user_current = request.user
    user_list = User.objects.exclude(pk=user_current.pk)
    if request.method == 'POST':
        form = forms.RoomAddForm(request.POST, user_list=user_list)
        if form.is_valid():
            room_name = request.POST['name']
            room_users = request.POST.getlist('room_members')
            room_new = models.Room(name=room_name)
            room_new.save()
            room_new.users.add(user_current)
            for user_pk in room_users:
                room_new.users.add(user_pk)
            return redirect('chat:index')
        else:
            return render(request, 'chat/room_add.html', {'form': form})
    else:
        form = forms.RoomAddForm(user_list=user_list)
        return render(request, 'chat/room_add.html', {'form': form})


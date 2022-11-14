from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from chat import forms


def index(request):
    user = request.user
    if user.is_authenticated:
        user_list = User.objects.exclude(pk=request.user.pk)
        return render(request, 'chat/index.html', {'user_list': user_list})
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


def room_view(request):
    return render(request, 'chat/room.html')


def room_add(request):
    user_list = User.objects.exclude(pk=request.user.pk)
    if request.method == 'POST':
        form = forms.RoomAddForm(request.POST, user_list=user_list)
        if form.is_valid():
            return redirect('chat:room_view')
        else:
            return render(request, 'chat/room_add.html', {'form': form})
    else:
        form = forms.RoomAddForm(user_list=user_list)
        return render(request, 'chat/room_add.html', {'form': form})


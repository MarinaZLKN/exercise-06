from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'chat/index.html')
    else:
        return redirect('chat:login_view')


def login_view(request):
    form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})
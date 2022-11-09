from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'chat/index.html')
    else:
        return redirect('chat:login_view')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return render(request, 'chat/login.html', {'form': form})
        else:
            return render(request, 'chat/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'chat/login.html', {'form': form})


def register_view(request):
    return render(request, 'chat/register.html', {'form': UserCreationForm()})

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from threeK_game.forms import RegisterForm
from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return render(request, "threeK_game/index.html")

def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, "threeK_game/home.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/home')
            else:
                return render(request, 'registration/signup.html', {'form': form})
        else:
            form = RegisterForm()
        return render(request, 'registration/signup.html', {'form': form})


def game(request):
    return render(request, 'threeK_game/game.html')

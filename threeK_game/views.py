from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from threeK_game.forms import RegisterForm
from django.shortcuts import render, redirect
from .models import Profile, Game
from django.db.models import Q
from django.http import HttpResponse

import json

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

def profile(request, username):

    try:
        profile = Profile.objects.get(user__username=username)
    except:
        return redirect('three_k:home')

    games = Game.objects.all().filter(Q(match__playerA=profile) | Q(match__playerB=profile)).order_by('-id')
    won_matches_as_player_a = profile.matches_as_player_a.filter(game__result=1).count()
    won_matches_as_player_b = profile.matches_as_player_b.filter(game__result=2).count()
    draw_matches = games.filter(result=0).count()

    won = won_matches_as_player_a + won_matches_as_player_b
    lost = games.count() - won - draw_matches

    return render(request, 'threeK_game/profile.html', {'profile': profile, 'games': games[:10], 'won': won, 'lost': lost})

def last_games(request):
    last_games = Game.objects.all().filter(Q(result=0) | Q(result=1) | Q(result=2)).order_by('-id')[:10]

    return render(request, 'threeK_game/last-games.html', {'games': last_games})

def game_o(request, id):
    try:
        game = Game.objects.get(pk=id)
    except:
        return redirect('three_k:home')

    if request.is_ajax():
        moves = game.moves

        return HttpResponse(game.moves if game.moves else json.dumps({}), content_type='application/json')

    return render(request, 'threeK_game/game-obs.html')

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

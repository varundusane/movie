from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, PlaylistForm
from .models import Playlist, movie_playlist
import requests
from .utils import generate_id


#################### index#######################################
@login_required(login_url='/login')
def index(request):
    us = request.user
    print(us)
    if request.method == 'POST':
        t = request.POST['t']
        url = 'http://www.omdbapi.com/?t=' + t + '&apikey=30c69399'
        response = requests.get(url)
        flag = 0
        if response.status_code == 200:
            flag = 1
            print("sucessfully fetched the data")
            print(response.json())
            img = response.json()['Poster']
            title = response.json()['Title']
            genre = response.json()['Genre']
            plot = response.json()['Plot']
            return render(request, 'index.html',
                          {'title': 'index', 'movie': title, 'poster': img, 'genre': genre, 'plot': plot, 'flag': flag})
        else:
            print(f"Hello person, there's a {response.status_code} error with your request")
        return render(request, 'index.html', {'title': 'index'})

    else:

        return render(request, 'index.html', {'title': 'index'})


def add_to_playlist(request, movie):
    u = request.user
    play = Playlist.objects.filter(user=u)
    return render(request, 'playlists.html', {'title': 'index', 'play': play, 'movie': movie})


def playlist(request):
    u = request.user
    play = Playlist.objects.filter(user=u)
    return render(request, 'playlists.html', {'title': 'index', 'play': play})


def add_movie_playlist(request, movie, pk):
    p = Playlist.objects.get(pk=pk)
    m = movie_playlist(playlist=p, movie_name=movie)
    m.save()
    return redirect('index')


def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            try:
                f = form.save(commit=False)
                print(f.public, f.playlist_name)

                f.playlist_name = f.playlist_name

            except Playlist.DoesNotExist:
                pass
            f.user = request.user
            f.url = request.user.username + form.cleaned_data.get('playlist_name')
            f.save()

            return redirect('index')
    else:
        form = PlaylistForm()
    return render(request, 'create_playlist.html', {'form': form, 'title': 'Create Playlist'})


########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'register here'})


################ login forms###################################################
def Login(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'log in'})

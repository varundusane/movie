from django.contrib.auth.models import User
from django.db import models


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=30)
    public = models.BooleanField(default=False)
    url = models.CharField(max_length=100)


class movie_playlist(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=100)

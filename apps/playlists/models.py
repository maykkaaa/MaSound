from django.db import models
from django.contrib.auth.models import User
from apps.tracks.models import Track
class Playlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    title = models.CharField(max_length=120)
    tracks = models.ManyToManyField(Track, blank=True, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

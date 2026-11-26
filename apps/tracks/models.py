from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
class Track(models.Model):
    title = models.CharField(max_length=160)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracks")
    audio = models.FileField(upload_to="tracks/")
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    plays = models.PositiveIntegerField(default=0)
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse("track_detail", args=[self.pk])
    @property
    def likes_count(self): return self.likes.count()

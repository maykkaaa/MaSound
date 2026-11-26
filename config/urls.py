from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views
from apps.accounts.views import signup
from apps.accounts.views import (
    signup,
    edit_profile,
    my_profile,
    public_profile
)

urlpatterns = [
path('admin/',admin.site.urls), path('',views.home,name='home'),
path('accounts/signup/',signup,name='signup'), path('accounts/',include('django.contrib.auth.urls')),
path('upload/',views.upload_track,name='upload'), path('track/<int:pk>/',views.track_detail,name='track_detail'),
path('track/<int:pk>/like/',views.toggle_like,name='toggle_like'),
path('playlists/create/',views.create_playlist,name='create_playlist'), path('playlists/<int:pk>/',views.playlist_detail,name='playlist_detail'),
path(
    "track/<int:pk>/edit/",
    views.edit_track,
    name="edit_track"
),

path(
    "track/<int:pk>/delete/",
    views.delete_track,
    name="delete_track"
),

path(
    "profile/",
    my_profile,
    name="my_profile"
),

path(
    "profile/edit/",
    edit_profile,
    name="edit_profile"
),

path(
    "user/<str:username>/",
    public_profile,
    name="public_profile"
),
]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

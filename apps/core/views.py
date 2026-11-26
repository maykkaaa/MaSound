from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from apps.tracks.models import Track
from apps.social.models import Like, Comment
from apps.playlists.models import Playlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    q=request.GET.get('q','').strip()
    tracks=Track.objects.select_related('artist').order_by('-created_at')
    if q: tracks=tracks.filter(Q(title__icontains=q)|Q(artist__username__icontains=q)|Q(genre__icontains=q))
    return render(request,'core/home.html',{'tracks':tracks,'query':q})

def track_detail(request, pk):
    track=get_object_or_404(Track.objects.select_related('artist'),pk=pk)
    if request.method=='POST':
        if not request.user.is_authenticated: return redirect('login')
        body=request.POST.get('body','').strip()
        if body: Comment.objects.create(user=request.user,track=track,body=body)
    liked=request.user.is_authenticated and Like.objects.filter(user=request.user,track=track).exists()
    return render(request,'core/track_detail.html',{'track':track,'liked':liked})

@login_required
def toggle_like(request,pk):
    track=get_object_or_404(Track,pk=pk)
    like,created=Like.objects.get_or_create(user=request.user,track=track)
    if not created: like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def upload_track(request):
    if request.method=='POST':
        title=request.POST.get('title','').strip(); audio=request.FILES.get('audio')
        if title and audio and audio.name.lower().endswith(('.mp3','.wav','.ogg','.m4a')):
            track=Track.objects.create(title=title,artist=request.user,audio=audio,cover=request.FILES.get('cover'),genre=request.POST.get('genre',''),description=request.POST.get('description',''))
            messages.success(request,'Your track has been uploaded!')
            return redirect('track_detail',pk=track.pk)
        messages.error(request,'Add a title and a supported audio file (MP3, WAV, OGG or M4A).')
    return render(request,'core/upload.html')

@login_required
def create_playlist(request):
    if request.method=='POST':
        title=request.POST.get('title','').strip()
        if title:
            p=Playlist.objects.create(owner=request.user,title=title)
            return redirect('playlist_detail',pk=p.pk)
    return render(request,'core/create_playlist.html')

def playlist_detail(request,pk):
    playlist=get_object_or_404(Playlist.objects.select_related('owner'),pk=pk)
    if request.method=='POST' and request.user==playlist.owner:
        track=get_object_or_404(Track,pk=request.POST.get('track_id'))
        playlist.tracks.add(track)
    return render(request,'core/playlist_detail.html',{'playlist':playlist,'available_tracks':Track.objects.exclude(playlists=playlist)})


@login_required
def edit_track(request, pk):
    track = get_object_or_404(Track, pk=pk)

    if track.artist != request.user:
        messages.error(request, "You cannot edit this track.")
        return redirect("track_detail", pk=pk)

    if request.method == "POST":
        track.title = request.POST.get("title", "").strip()
        track.genre = request.POST.get("genre", "").strip()
        track.description = request.POST.get("description", "").strip()

        if request.FILES.get("audio"):
            track.audio = request.FILES["audio"]

        if request.FILES.get("cover"):
            track.cover = request.FILES["cover"]

        track.save()

        messages.success(request, "Track updated!")
        return redirect("track_detail", pk=track.pk)

    return render(request, "core/edit_track.html", {
        "track": track
    })


@login_required
def delete_track(request, pk):
    track = get_object_or_404(Track, pk=pk)

    if track.artist != request.user:
        messages.error(request, "You cannot delete this track.")
        return redirect("track_detail", pk=pk)

    if request.method == "POST":
        track.delete()
        messages.success(request, "Track deleted!")
        return redirect("home")

    return render(request, "core/delete_track.html", {
        "track": track
    })
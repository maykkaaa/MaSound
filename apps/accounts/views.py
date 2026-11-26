from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile
from .forms import ProfileEditForm


def signup(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        Profile.objects.get_or_create(user=user)

        login(request, user)

        return redirect("home")

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your profile has been updated!"
            )

            return redirect("my_profile")

    else:
        form = ProfileEditForm(user=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {"form": form, "profile": profile}
    )


@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "profile_user": request.user
        }
    )


def public_profile(request, username):
    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile, created = Profile.objects.get_or_create(
        user=profile_user
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "profile_user": profile_user
        }
    )

from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileEditForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    display_name = forms.CharField(
        max_length=100,
        required=False,
        label="Display name"
    )

    bio = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Tell us about yourself..."
        }),
        label="Bio"
    )

    avatar = forms.ImageField(
        required=False,
        label="Profile picture"
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if user:
            profile, created = Profile.objects.get_or_create(
                user=user
            )

            self.fields["username"].initial = user.username
            self.fields["display_name"].initial = profile.display_name
            self.fields["bio"].initial = profile.bio

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(
            username__iexact=username
        ).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def save(self):
        profile, created = Profile.objects.get_or_create(
            user=self.user
        )

        self.user.username = self.cleaned_data["username"]
        self.user.save()

        profile.display_name = self.cleaned_data["display_name"]
        profile.bio = self.cleaned_data["bio"]

        if self.cleaned_data.get("avatar"):
            profile.avatar = self.cleaned_data["avatar"]

        profile.save()

        return profile

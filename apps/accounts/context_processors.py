from .models import Profile

def user_profile(request):
    profile = None

    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

    return {
        "current_profile": profile
    }
"apps.accounts.context_processors.user_profile",

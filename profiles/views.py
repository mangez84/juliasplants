from django.shortcuts import render


def profile(request):
    """Return the profile page."""
    template = 'profiles/profile.html'
    return render(request, template)

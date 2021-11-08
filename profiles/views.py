from django.shortcuts import render
from .models import UserProfile


def save_profile(request, form):
    """Save profile information"""
    UserProfile.objects.create(
        user=request.user,
        address=form.cleaned_data['address'],
        city=form.cleaned_data['city'],
        postcode=form.cleaned_data['postcode'],
        country=form.cleaned_data['country'],
        phone_number=form.cleaned_data['phone_number'],
    )


def profile(request):
    """Return the profile page."""
    template = 'profiles/profile.html'
    return render(request, template)

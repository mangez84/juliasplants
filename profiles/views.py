from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserForm, UserProfileForm


def save_profile(request, form):
    """Save profile information."""
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
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    user_form = UserForm(instance=user)
    profile_form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders
    }
    template = 'profiles/profile.html'
    return render(request, template, context)

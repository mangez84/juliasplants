from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserForm, UserProfileForm, UserProfileCommentForm


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


def show_profile(request):
    """Return the profile page."""
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    user_form = UserForm(instance=user, prefix='user_form')
    profile_form = UserProfileForm(instance=profile, prefix='profile_form')
    comment_form = UserProfileCommentForm()
    orders = profile.orders.all()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'comment_form': comment_form,
        'orders': orders
    }
    template = 'profiles/profile.html'
    return render(request, template, context)


def edit_profile(request):
    """Edit profile information."""
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)
        user_form = UserForm(request.POST, instance=user, prefix='user_form')
        profile_form = UserProfileForm(
            request.POST, instance=profile, prefix='profile_form')
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Details successfully updated.')
            return redirect('show_profile')
        messages.error(
            request,
            'Could not update details. Please ensure form is valid.')
        return redirect('show_profile')

    return redirect('show_profile')

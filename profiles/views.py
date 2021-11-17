import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile, UserProfileComment
from .forms import UserForm, UserProfileForm, UserProfileCommentForm


def save_profile(request, form):
    """Save profile information after checkout."""
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

    try:
        profile = UserProfile.objects.get(user__username=user)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(
            user=request.user,
            address='',
            city='',
            postcode='',
            country='',
            phone_number='',
        )
        profile = UserProfile.objects.get(user__username=user)

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
            messages.success(
                request,
                'The user information has been updated.')
            return redirect('show_profile')
        messages.error(
            request,
            'Could not update user information. Please ensure form is valid.')
        return redirect('show_profile')

    return redirect('show_profile')


def add_comment(request):
    """Add user comments and ratings."""
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)
        comment_form = UserProfileCommentForm(request.POST)
        if comment_form.is_valid():
            valid_form = comment_form.save(commit=False)
            valid_form.profile = profile
            valid_form.save()
            messages.success(request, 'Thank you for reviewing us!')
            return redirect('show_profile')
        messages.error(
            request,
            'Could not send the review. Please ensure form is valid.')
        return redirect('show_profile')

    return redirect('show_profile')


def get_comments(request):
    """Return a number of random user comments."""
    if request.method == 'GET':
        try:
            comments = list(UserProfileComment.objects.all())
            num_comments = len(comments)
            if num_comments == 0:
                random_comments = None
            if 1 <= num_comments < 3:
                random_comments = random.sample(comments, num_comments)
            if num_comments >= 3:
                random_comments = random.sample(comments, 3)
        except ValueError:
            random_comments = None

        return random_comments
    return redirect('home')

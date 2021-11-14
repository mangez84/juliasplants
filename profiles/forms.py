from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserProfileComment


class UserForm(forms.ModelForm):
    """Form for updates in the user model."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    """Form for updates in the user profile model."""
    class Meta:
        model = UserProfile
        fields = (
            'address', 'city', 'postcode', 'country', 'phone_number',)


class UserProfileCommentForm(forms.ModelForm):
    """Form for creation of user comments."""
    class Meta:
        model = UserProfileComment
        fields = ('title', 'comment', 'rating')
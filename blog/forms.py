from django import forms
from .models import BlogPost


class BlogForm(forms.ModelForm):
    """Form for updates in the plant model."""
    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'plant',)

from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    """Form for updates in the plant model."""
    class Meta:
        model = Plant
        fields = ('name', 'botanical_name', 'description',
                  'price', 'discount_price', 'category', 'image',)

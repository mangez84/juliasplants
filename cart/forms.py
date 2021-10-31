from django import forms


class CartForm(forms.Form):
    quantity = forms.CharField(
        label='Quantity',
        widget=forms.TextInput(attrs={'min': 1, 'max': 5, 'type': 'number'})
    )

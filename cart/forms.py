from django import forms


class CartForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantity',
        initial=1,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput()
    )

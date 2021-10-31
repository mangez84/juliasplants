from django.shortcuts import render, redirect, get_object_or_404
from .forms import CartForm
from plants.models import Plant


def show_cart(request):
    """Return the page for the shopping cart."""
    template = 'cart/cart.html'
    return render(request, template)


def add_to_cart(request, plant_id):
    """Add a plant to the cart"""
    plant = get_object_or_404(Plant, pk=plant_id)
    print(plant)
    redirect_url = request.POST.get('redirect_url')
    form = CartForm(request.POST)
    if form.is_valid():
        print(form)
    return redirect(redirect_url)

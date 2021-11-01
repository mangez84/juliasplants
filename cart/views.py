from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import Coalesce
from .forms import CartForm
from plants.models import Plant


def show_cart(request):
    """Return the page for the shopping cart."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_cost = 0
    for plant_id, quantity in cart.items():
        plant = get_object_or_404(Plant, pk=plant_id)
        if request.user.is_authenticated:
            if plant.discount_price:
                price = plant.discount_price
            else:
                price = plant.price
        else:
            price = plant.price
        total_cost += quantity * price
        cart_items.append({
            'plant': plant,
            'quantity': quantity,
        })
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    template = 'cart/cart.html'
    return render(request, template, context)


def add_to_cart(request, plant_id):
    """Add a plant with the desired quantity to the cart"""
    if request.method == 'POST':
        plant = get_object_or_404(Plant, pk=plant_id)
        form = CartForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart', {})
            if plant_id in list(cart.keys()):
                cart[plant_id] += form.cleaned_data['quantity']
            else:
                cart[plant_id] = form.cleaned_data['quantity']
            print(cart)
        request.session['cart'] = cart
        return redirect('plant_details', plant_id=plant.id)
    return redirect('plant_details', plant_id=plant.id)

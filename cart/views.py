from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from plants.models import Plant


def show_cart(request):
    """Return the page for the shopping cart."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    total_cost = 0
    if len(cart) > 0:
        for plant_id, quantity in cart.items():
            plant = get_object_or_404(Plant, pk=plant_id)
            if request.user.is_authenticated:
                if plant.discount_price:
                    price = plant.discount_price
                else:
                    price = plant.price
            else:
                price = plant.price
            total = quantity * price
            total_cost += quantity * price
            cart_items.append({
                'plant': plant,
                'quantity': quantity,
                'price': price,
                'total': total,
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
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity'))
        if plant_id in list(cart.keys()):
            cart[plant_id] += quantity
        else:
            cart[plant_id] = quantity
        messages.success(
            request,
            f'{quantity} x {plant.name} successfully added to cart.'
        )
        request.session['cart'] = cart
        return redirect('plant_details', plant_id=plant.id)
    return redirect('plant_details', plant_id=plant.id)


def edit_cart(request):
    """Edit the cart with updated quantities."""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for plant_id in cart:
            new_quantity = f'quantity-{plant_id}'
            quantity = int(request.POST.get(new_quantity))
            cart[plant_id] = quantity
        request.session['cart'] = cart
        messages.success(request, 'Cart was successfully updated.')
        return redirect('show_cart')
    return redirect('show_cart')


def del_from_cart(request, plant_id):
    """Delete a plant from the cart."""
    if request.method == 'POST':
        plant = get_object_or_404(Plant, pk=plant_id)
        cart = request.session.get('cart', {})
        cart.pop(plant_id)
        request.session['cart'] = cart
        messages.success(
            request,
            f'{plant.name} was successfully deleted from the cart.'
        )
        return HttpResponse(status=200)
    return redirect('show_cart')

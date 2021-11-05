from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderForm
from cart.views import get_cart_items
import stripe


def checkout(request):
    """Checkout and place order."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        return redirect('cart')
    cart_items, total_cost = get_cart_items(request)
    form = OrderForm()
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'form': form,
    }
    template = 'checkout/checkout.html'
    return render(request, template, context)

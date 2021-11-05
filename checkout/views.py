from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import stripe
from cart.views import get_cart_items
from .models import Order, OrderItem
from .forms import OrderForm


def checkout(request):
    """Checkout and save the order."""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart_items, total_cost = get_cart_items(request)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_cost = total_cost
            order.stripe_pid = (
                request.POST.get('client_secret').split('_secret')[0])
            order.save()
            for cart_item in cart_items:
                order_item = OrderItem(
                    order=order,
                    plant=cart_item['plant'],
                    quantity=cart_item['quantity'],
                    total=cart_item['total'],
                )
                order_item.save()
        return redirect('show_cart')

    cart_items, total_cost = get_cart_items(request)
    stripe_total = round(total_cost * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.user.is_authenticated:
        form = OrderForm(initial={
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@test.com',
            'address': 'Test',
            'city': 'Test',
            'postcode': 'Test',
            'country': 'SE',
            'phone_number': 'Test',
        })
    else:
        form = OrderForm()

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    template = 'checkout/checkout.html'
    return render(request, template, context)

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
import stripe
from cart.views import get_cart_items
from profiles.models import UserProfile
from profiles.views import save_profile
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
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    order.profile = profile
                    order.save()
                except UserProfile.DoesNotExist:
                    save_profile(request, form)
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
            del request.session['cart']
            return redirect('checkout_confirm', order_uuid=order.order_uuid)
        else:
            messages.error(
                request, 'Checkout failed. Please ensure form is valid.')
            return redirect('checkout')

    cart_items, total_cost = get_cart_items(request)
    stripe_total = round(total_cost * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = OrderForm(initial={
                'first_name': profile.user.first_name,
                'last_name': profile.user.last_name,
                'email': profile.user.email,
                'address': profile.address,
                'city': profile.city,
                'postcode': profile.postcode,
                'country': profile.country,
                'phone_number': profile.phone_number,
            })
        except UserProfile.DoesNotExist:
            form = OrderForm(initial={
                'email': request.user.email,
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


def checkout_confirm(request, order_uuid):
    """Show the user an order confirmation"""
    order = get_object_or_404(Order, order_uuid=order_uuid)
    context = {
        'order': order,
    }
    template = 'checkout/checkout_confirm.html'
    return render(request, template, context)

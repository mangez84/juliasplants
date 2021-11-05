from django.shortcuts import render


def checkout(request):
    """Checkout and place order."""
    template = 'checkout/checkout.html'
    return render(request, template)

from django.shortcuts import render


def home(request):
    """Return the home page."""
    template = 'home/home.html'
    return render(request, template)

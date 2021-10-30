from django.shortcuts import render


def get_plants(request):
    """Return all plants."""
    template = 'plants/plants.html'
    return render(request, template)

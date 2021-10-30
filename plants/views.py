from django.shortcuts import render
from .models import Plant, Category


def get_plants(request):
    """Return all plants."""
    plants = Plant.objects.all()
    print(plants)
    context = {
        'plants': plants,
    }
    template = 'plants/plants.html'
    return render(request, template, context)

from django.shortcuts import render
from django.db.models.functions import Coalesce
from .models import Plant, Category


def get_plants(request):
    """Return all plants."""
    plants = Plant.objects.all()
    sort = {
        'key': None,
        'direction': None,
    }

    if request.GET:
        if 'sort' in request.GET:
            sort['key'] = request.GET['sort']
            sort['direction'] = request.GET['direction']
            if sort['direction'] == 'asc':
                if sort['key'] == 'name':
                    plants = plants.order_by(sort['key'])
                else:
                    plants = plants.order_by(
                        Coalesce('discount_price', sort['key']))
            else:
                if sort['key'] == 'name':
                    plants = plants.order_by(sort['key']).reverse()
                else:
                    plants = plants.order_by(
                        Coalesce('discount_price', sort['key'])).reverse()

    context = {
        'plants': plants,
        'sort': sort,
    }
    template = 'plants/plants.html'
    return render(request, template, context)

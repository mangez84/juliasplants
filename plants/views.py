from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Coalesce
from .models import Plant


def get_plants(request):
    """Return all plants."""
    plants = Plant.objects.all()
    sort = {'key': None, 'direction': None}

    if request.GET:
        if 'sort' in request.GET:
            sort['key'] = request.GET['sort']
            sort['direction'] = request.GET['direction']
            if sort['direction'] == 'asc':
                if sort['key'] == 'price':
                    plants = plants.order_by(
                        Coalesce('discount_price', sort['key']))
                elif sort['key'] == 'category':
                    plants = plants.order_by(f"{sort['key']}__name")
                else:
                    plants = plants.order_by(sort['key'])
            else:
                if sort['key'] == 'price':
                    plants = plants.order_by(
                        Coalesce('discount_price', sort['key'])).reverse()
                elif sort['key'] == 'category':
                    plants = plants.order_by(f"{sort['key']}__name").reverse()
                else:
                    plants = plants.order_by(sort['key']).reverse()
        if 'category' in request.GET:
            category = request.GET['category']
            if category == 'discounted_plants':
                plants = plants.filter(discount_price__isnull=False)
            else:
                plants = plants.filter(category__filter_name=category)
        if 'query' in request.GET:
            query = request.GET['query']
            plants = plants.filter(
                Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'plants': plants,
        'sort': sort,
    }
    template = 'plants/plants.html'
    return render(request, template, context)

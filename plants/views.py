from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.db.models.functions import Coalesce
from profiles.views import get_comments
from .models import Plant


def sort_plants(plants, sort):
    """Sort the plants."""
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
    return plants


def show_plants(request):
    """Return all plants."""
    plants = Plant.objects.all()
    comments = get_comments(request)
    sort = {'key': None, 'direction': None}

    if request.GET:
        if 'sort' in request.GET:
            sort['key'] = request.GET['sort']
            sort['direction'] = request.GET['direction']
            plants = sort_plants(plants, sort)
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
        'comments': comments,
        'sort': sort,
    }
    template = 'plants/plants.html'
    return render(request, template, context)


def plant_details(request, plant_id):
    """Return details for a specific plant."""
    plant = get_object_or_404(Plant, pk=plant_id)
    context = {
        'plant': plant,
    }
    template = 'plants/plant_details.html'
    return render(request, template, context)

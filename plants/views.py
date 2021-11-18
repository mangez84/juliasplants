from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Coalesce
from profiles.views import get_comments
from .models import Plant
from .forms import PlantForm


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


@login_required
def add_plant(request):
    """Add a plant to the database."""
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators may add plants.')
        return redirect('home')

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added plant.')
            return redirect('plants')

        messages.error(
            request,
            'Failed to add plant. Please ensure the form is valid.'
        )
        return redirect('plants')

    form = PlantForm()
    context = {
        'form': form,
    }
    template = 'plants/add_plant.html'
    return render(request, template, context)


@login_required
def edit_plant(request, plant_id):
    """Edit details for a specific plant."""
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators may edit plants.')
        return redirect('home')

    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated plant.')
            return redirect('plant_details', plant_id=plant.id)

        messages.error(
            request,
            'Failed to update plant. Please ensure the form is valid.'
        )
        return redirect('plants')

    form = PlantForm(instance=plant)
    context = {
        'plant': plant,
        'form': form,
    }
    template = 'plants/edit_plant.html'
    return render(request, template, context)

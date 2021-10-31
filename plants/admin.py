from django.contrib import admin
from .models import Plant, Category


class PlantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'botanical_name',
        'description',
        'price',
        'discount_price',
        'image',
        'category',
    )
    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'filter_name',
    )
    ordering = ('name',)


admin.site.register(Plant, PlantAdmin)
admin.site.register(Category, CategoryAdmin)

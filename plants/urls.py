from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_plants, name='plants'),
    path('<int:plant_id>/', views.plant_details, name='plant_details'),
    path('edit_plant/<int:plant_id>/', views.edit_plant, name='edit_plant'),
]

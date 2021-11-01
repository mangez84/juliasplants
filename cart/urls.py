from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('add/<plant_id>/', views.add_to_cart, name='add_to_cart'),
]
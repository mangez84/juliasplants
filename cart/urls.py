from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('add/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('edit/', views.edit_cart, name='edit_cart'),
    path('delete/<int:plant_id>/', views.del_from_cart, name='del_from_cart'),
]

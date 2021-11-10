from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('confirmation/<order_uuid>',
         views.checkout_confirm, name='checkout_confirm'),
]

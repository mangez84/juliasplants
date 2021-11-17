from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('confirmation/<order_uuid>', views.checkout_confirm,
         name='checkout_confirm'),
    path('modify_stripe_data/', views.modify_stripe_data,
         name='modify_stripe_data'),
    path('webhook/', webhook, name='webhook'),
]

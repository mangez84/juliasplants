from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_profile, name='show_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

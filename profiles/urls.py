from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_profile, name='show_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_comment/', views.add_comment, name='add_comment'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_blog_posts, name='show_blog_posts'),
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'),
    path('edit_blog_post/<int:blog_post_id>/',
         views.edit_blog_post, name='edit_blog_post'),
    path('del_blog_post/<int:blog_post_id>/',
         views.del_blog_post, name='del_blog_post'),
]

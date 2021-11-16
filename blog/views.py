from django.shortcuts import render
from .models import BlogPost


def show_blog_posts(request):
    """Return blog posts."""
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts,
    }
    template = 'blog/blog_posts.html'
    return render(request, template, context)

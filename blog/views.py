from django.shortcuts import render


def show_blog_posts(request):
    """Return blog posts."""
    template = 'blog/blog_posts.html'
    return render(request, template)

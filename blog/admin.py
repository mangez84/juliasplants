from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    """Display blog posts on the admin site."""
    list_display = ('title', 'body', 'date', 'profile', 'plant',)
    ordering = ('-date',)


admin.site.register(BlogPost, BlogPostAdmin)

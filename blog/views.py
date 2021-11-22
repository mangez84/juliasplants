from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from .models import BlogPost
from .forms import BlogForm


def show_blog_posts(request):
    """Return blog posts."""
    blog_posts = BlogPost.objects.all()
    context = {
        'blog_posts': blog_posts,
    }
    template = 'blog/blog_posts.html'
    return render(request, template, context)


def blog_post_details(request, blog_post_id):
    """Return details for a specific plant."""
    blog_post = get_object_or_404(BlogPost, pk=blog_post_id)
    context = {
        'blog_post': blog_post,
    }
    template = 'blog/blog_post_details.html'
    return render(request, template, context)


@login_required
def add_blog_post(request):
    """Add a blog post to the database."""
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators may add blog posts.')
        return redirect('home')

    try:
        profile = UserProfile.objects.get(user__username=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Sorry, you must update your profile first!')
        return redirect('show_profile')

    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            valid_form = form.save(commit=False)
            valid_form.profile = profile
            form.save()
            messages.success(request, 'Successfully added blog post.')
            return redirect('show_blog_posts')

        messages.error(
            request,
            'Failed to add blog post. Please ensure the form is valid.'
        )
        return redirect('show_blog_posts')

    form = BlogForm()
    context = {
        'form': form,
    }
    template = 'blog/add_blog_post.html'
    return render(request, template, context)


@login_required
def edit_blog_post(request, blog_post_id):
    """Edit details for a specific blog post."""
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators may edit blog posts.')
        return redirect('home')

    blog_post = get_object_or_404(BlogPost, pk=blog_post_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated blog post.')
            return redirect('show_blog_posts')

        messages.error(
            request,
            'Failed to update blog post. Please ensure the form is valid.'
        )
        return redirect('show_blog_posts')

    form = BlogForm(instance=blog_post)
    context = {
        'blog_post': blog_post,
        'form': form,
    }
    template = 'blog/edit_blog_post.html'
    return render(request, template, context)


@login_required
def del_blog_post(request, blog_post_id):
    """Delete a specific blog post."""
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators may delete blog posts.')
        return redirect('home')

    blog_post = get_object_or_404(BlogPost, pk=blog_post_id)
    context = {
        'blog_post': blog_post,
    }

    if request.method == 'POST':
        blog_post.delete()
        messages.success(request, 'Successfully deleted blog post.')
        return redirect('show_blog_posts')

    template = 'blog/del_blog_post.html'
    return render(request, template, context)

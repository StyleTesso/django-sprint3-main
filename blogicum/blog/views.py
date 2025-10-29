from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.utils import timezone

from .models import Category, Post


VALUE_POSTS = 5


def get_published_posts():
    """Function for getting QuerySet posts."""
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('author', 'category', 'location')


def index(request):
    """Passing the entire list of posts to the context."""
    template = 'blog/index.html'
    post_list = get_published_posts()[:VALUE_POSTS]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id: int) -> HttpResponse:
    """Passing the entire list of posts to the context."""
    template = 'blog/detail.html'
    post = get_object_or_404(get_published_posts(), pk=post_id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Passing the entire list of posts to the context."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    post_list = get_published_posts().filter(category=category)
    return render(request, template,
                  {'category': category, 'post_list': post_list})

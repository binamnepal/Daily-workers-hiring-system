from django.shortcuts import get_object_or_404, render

from .services import CategoryService


def category_list(request):
    categories = CategoryService.list_active()
    return render(request, "categories/list.html", {"categories": categories})


def category_detail(request, slug):
    category = CategoryService.get_by_slug(slug)
    return render(request, "categories/detail.html", {"category": category})

from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.category_list, name="list"),
    path("categories/<slug:slug>/", views.category_detail, name="detail"),
]

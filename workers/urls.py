from django.urls import path

from . import views

app_name = "workers"

urlpatterns = [
    path("search/", views.worker_search, name="search"),
    path("me/", views.my_profile, name="my_profile"),
    path("me/availability/", views.add_availability, name="add_availability"),
    path("<uuid:id>/", views.worker_detail, name="detail"),
    path("search/", views.search, name="search"),
]

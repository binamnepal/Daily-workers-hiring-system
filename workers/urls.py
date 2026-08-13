from django.urls import path

from . import views

app_name = "workers"

urlpatterns = [
    path("search/", views.WorkerSearchView.as_view(), name="search"),
    path("me/", views.MyWorkerProfileView.as_view(), name="me"),
    path("me/availability/", views.AddAvailabilityView.as_view(), name="add-availability"),
    path("me/available/", views.SetAvailableView.as_view(), name="set-available"),
    path("<uuid:id>/", views.WorkerDetailView.as_view(), name="detail"),
]

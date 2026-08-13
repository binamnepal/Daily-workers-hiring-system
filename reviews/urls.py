from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("bookings/<uuid:booking_id>/review/", views.CreateReviewView.as_view(), name="create"),
    path("workers/<uuid:worker_id>/", views.WorkerReviewsView.as_view(), name="worker-reviews"),
]

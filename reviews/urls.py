from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("bookings/<uuid:booking_id>/review/", views.create_review, name="create"),
    path("workers/<uuid:worker_id>/", views.worker_reviews, name="worker_reviews"),
]

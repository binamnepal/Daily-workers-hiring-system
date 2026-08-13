from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("create/", views.create_booking, name="create"),
    path("mine/", views.my_bookings, name="mine"),
    path("<uuid:id>/", views.booking_detail, name="detail"),
    path("<uuid:id>/assign/", views.assign_worker, name="assign"),
    path("<uuid:id>/accept/", views.accept_booking, name="accept"),
    path("<uuid:id>/reject/", views.reject_booking, name="reject"),
    path("<uuid:id>/start/", views.start_booking, name="start"),
    path("<uuid:id>/complete/", views.complete_booking, name="complete"),
    path("<uuid:id>/cancel/", views.cancel_booking, name="cancel"),
]

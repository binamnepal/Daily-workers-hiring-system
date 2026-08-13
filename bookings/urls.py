from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.CreateBookingView.as_view(), name="create"),
    path("mine/", views.MyBookingsView.as_view(), name="mine"),
    path("<uuid:id>/", views.BookingDetailView.as_view(), name="detail"),
    path("<uuid:id>/assign/", views.AssignWorkerView.as_view(), name="assign"),
    path("<uuid:id>/accept/", views.AcceptBookingView.as_view(), name="accept"),
    path("<uuid:id>/reject/", views.RejectBookingView.as_view(), name="reject"),
    path("<uuid:id>/start/", views.StartBookingView.as_view(), name="start"),
    path("<uuid:id>/complete/", views.CompleteBookingView.as_view(), name="complete"),
    path("<uuid:id>/cancel/", views.CancelBookingView.as_view(), name="cancel"),
]

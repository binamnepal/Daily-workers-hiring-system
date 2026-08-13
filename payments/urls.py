from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("bookings/<uuid:booking_id>/pay/", views.CreatePaymentView.as_view(), name="create"),
    path("<uuid:payment_id>/charge/", views.ChargePaymentView.as_view(), name="charge"),
]

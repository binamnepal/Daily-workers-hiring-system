from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("bookings/<uuid:booking_id>/pay/", views.pay_for_booking, name="pay"),
    path("<uuid:payment_id>/charge/", views.charge_payment, name="charge"),
]

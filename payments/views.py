from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking

from .forms import ChargePaymentForm, CreatePaymentForm
from .models import Payment
from .services import PaymentService


@login_required
def pay_for_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    payment = getattr(booking, "payment", None)

    if payment is None:
        if request.method == "POST":
            form = CreatePaymentForm(request.POST)
            if form.is_valid():
                try:
                    payment = PaymentService.create_for_booking(booking=booking, **form.cleaned_data)
                except DjangoValidationError as exc:
                    messages.error(request, str(exc))
                    return redirect("bookings:detail", id=booking.id)
        else:
            form = CreatePaymentForm()
            return render(request, "payments/create.html", {"form": form, "booking": booking})

    charge_form = ChargePaymentForm()
    return render(request, "payments/detail.html", {"payment": payment, "booking": booking, "charge_form": charge_form})


@login_required
def charge_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, booking__customer=request.user)
    if request.method == "POST":
        form = ChargePaymentForm(request.POST)
        if form.is_valid():
            try:
                PaymentService.charge(payment=payment, **form.cleaned_data)
                messages.success(request, "Payment successful.")
            except DjangoValidationError as exc:
                messages.error(request, str(exc))
    return redirect("bookings:detail", id=payment.booking.id)

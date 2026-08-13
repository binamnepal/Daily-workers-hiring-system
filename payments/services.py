"""
Business logic for charging a customer once a booking is completed.
Kept provider-agnostic: PaymentService.charge() is where you'd plug in
a real gateway call (Stripe, Khalti, eSewa, etc.) behind provider_reference.
"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from bookings.models import Booking

from .models import Payment


class PaymentService:

    @staticmethod
    def create_for_booking(*, booking: Booking, method=Payment.Method.CASH):
        if booking.status != Booking.Status.COMPLETED:
            raise ValidationError("Payments can only be created for completed bookings.")
        if hasattr(booking, "payment"):
            raise ValidationError("A payment already exists for this booking.")
        amount = booking.final_price or booking.estimated_price
        if amount is None:
            raise ValidationError("Booking has no price set.")
        return Payment.objects.create(booking=booking, amount=amount, method=method)

    @staticmethod
    @transaction.atomic
    def charge(*, payment: Payment, provider_reference=""):
        if payment.status == Payment.Status.PAID:
            raise ValidationError("Payment already completed.")

        # Placeholder for real gateway integration.
        success = True

        if success:
            payment.status = Payment.Status.PAID
            payment.provider_reference = provider_reference
            payment.paid_at = timezone.now()
        else:
            payment.status = Payment.Status.FAILED
        payment.save(update_fields=["status", "provider_reference", "paid_at"])
        return payment

    @staticmethod
    def refund(*, payment: Payment):
        if payment.status != Payment.Status.PAID:
            raise ValidationError("Only paid payments can be refunded.")
        payment.status = Payment.Status.REFUNDED
        payment.save(update_fields=["status"])
        return payment

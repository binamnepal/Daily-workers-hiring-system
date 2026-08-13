"""
Business logic for leaving a review after a booking completes, and
keeping the worker's average_rating in sync.
"""
from django.core.exceptions import ValidationError
from django.db import transaction

from bookings.models import Booking
from workers.services import WorkerService

from .models import Review


class ReviewService:

    @staticmethod
    @transaction.atomic
    def create_review(*, booking: Booking, customer, rating, comment=""):
        if booking.customer_id != customer.id:
            raise ValidationError("Only the customer on this booking can leave a review.")
        if booking.status != Booking.Status.COMPLETED:
            raise ValidationError("Can only review a completed booking.")
        if hasattr(booking, "review"):
            raise ValidationError("This booking has already been reviewed.")
        if not (1 <= rating <= 5):
            raise ValidationError("rating must be between 1 and 5.")

        review = Review.objects.create(
            booking=booking, customer=customer, worker=booking.worker, rating=rating, comment=comment
        )
        WorkerService.recalculate_rating(booking.worker)
        return review

    @staticmethod
    def list_for_worker(worker):
        return Review.objects.filter(worker=worker).select_related("customer")

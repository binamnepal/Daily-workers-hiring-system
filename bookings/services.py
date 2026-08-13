"""
Business logic for the booking lifecycle:
create -> (assign) -> accepted -> in_progress -> completed
                    -> rejected
any non-terminal state -> cancelled

Views should only ever call BookingService; they should never mutate
Booking.status directly, so every transition is validated and logged
in one place.
"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from categories.models import ServiceCategory
from workers.models import WorkerProfile
from workers.services import WorkerService

from .models import Booking, BookingStatusLog

# Allowed status -> {allowed next statuses}
_TRANSITIONS = {
    Booking.Status.PENDING: {Booking.Status.ACCEPTED, Booking.Status.REJECTED, Booking.Status.CANCELLED},
    Booking.Status.ACCEPTED: {Booking.Status.IN_PROGRESS, Booking.Status.CANCELLED},
    Booking.Status.IN_PROGRESS: {Booking.Status.COMPLETED, Booking.Status.CANCELLED},
    Booking.Status.COMPLETED: set(),
    Booking.Status.CANCELLED: set(),
    Booking.Status.REJECTED: set(),
}


class BookingService:

    @staticmethod
    def _transition(booking: Booking, to_status, note=""):
        allowed = _TRANSITIONS.get(booking.status, set())
        if to_status not in allowed:
            raise ValidationError(
                f"Cannot move booking from '{booking.status}' to '{to_status}'."
            )
        from_status = booking.status
        booking.status = to_status
        booking.save(update_fields=["status", "updated_at"])
        BookingStatusLog.objects.create(
            booking=booking, from_status=from_status, to_status=to_status, note=note
        )
        return booking

    @staticmethod
    @transaction.atomic
    def create_booking(*, customer, category_slug, address, city, scheduled_start, notes="", worker_id=None):
        try:
            category = ServiceCategory.objects.get(slug=category_slug, is_active=True)
        except ServiceCategory.DoesNotExist:
            raise ValidationError("Unknown or inactive service category.")

        if scheduled_start <= timezone.now():
            raise ValidationError("scheduled_start must be in the future.")

        worker = None
        if worker_id:
            try:
                worker = WorkerProfile.objects.get(id=worker_id, is_available=True)
            except WorkerProfile.DoesNotExist:
                raise ValidationError("Selected worker is not available.")
            if not worker.skills.filter(id=category.id).exists():
                raise ValidationError("Selected worker does not offer this service category.")

        booking = Booking.objects.create(
            customer=customer,
            worker=worker,
            category=category,
            address=address,
            city=city,
            scheduled_start=scheduled_start,
            notes=notes,
            estimated_price=category.base_price,
        )
        BookingStatusLog.objects.create(
            booking=booking, from_status="", to_status=Booking.Status.PENDING, note="Booking created"
        )
        return booking

    @staticmethod
    def assign_worker(*, booking: Booking, worker: WorkerProfile):
        if booking.status != Booking.Status.PENDING:
            raise ValidationError("Can only assign a worker to a pending booking.")
        if not worker.is_available:
            raise ValidationError("Worker is not currently available.")
        if not worker.skills.filter(id=booking.category_id).exists():
            raise ValidationError("Worker does not offer this service category.")
        booking.worker = worker
        booking.save(update_fields=["worker", "updated_at"])
        return booking

    @staticmethod
    def accept(*, booking: Booking, worker: WorkerProfile):
        if booking.worker_id != worker.id:
            raise ValidationError("Only the assigned worker can accept this booking.")
        return BookingService._transition(booking, Booking.Status.ACCEPTED, note="Worker accepted")

    @staticmethod
    def reject(*, booking: Booking, worker: WorkerProfile, reason=""):
        if booking.worker_id != worker.id:
            raise ValidationError("Only the assigned worker can reject this booking.")
        booking = BookingService._transition(booking, Booking.Status.REJECTED, note=reason)
        booking.worker = None
        booking.save(update_fields=["worker"])
        return booking

    @staticmethod
    def start(*, booking: Booking, worker: WorkerProfile):
        if booking.worker_id != worker.id:
            raise ValidationError("Only the assigned worker can start this booking.")
        return BookingService._transition(booking, Booking.Status.IN_PROGRESS, note="Work started")

    @staticmethod
    @transaction.atomic
    def complete(*, booking: Booking, worker: WorkerProfile, final_price=None):
        if booking.worker_id != worker.id:
            raise ValidationError("Only the assigned worker can complete this booking.")
        booking = BookingService._transition(booking, Booking.Status.COMPLETED, note="Work completed")
        booking.final_price = final_price or booking.estimated_price
        booking.completed_at = timezone.now()
        booking.save(update_fields=["final_price", "completed_at"])
        WorkerService.record_completed_job(worker)
        return booking

    @staticmethod
    def cancel(*, booking: Booking, actor, reason=""):
        if actor != booking.customer and (booking.worker is None or actor != booking.worker.user):
            raise ValidationError("Only the customer or assigned worker can cancel this booking.")
        booking = BookingService._transition(booking, Booking.Status.CANCELLED, note=reason)
        booking.cancellation_reason = reason
        booking.cancelled_at = timezone.now()
        booking.save(update_fields=["cancellation_reason", "cancelled_at"])
        return booking

    @staticmethod
    def list_for_customer(customer):
        return Booking.objects.filter(customer=customer).select_related("category", "worker__user")

    @staticmethod
    def list_for_worker(worker: WorkerProfile):
        return Booking.objects.filter(worker=worker).select_related("category", "customer")

import uuid
from django.conf import settings
from django.db import models

from categories.models import ServiceCategory
from workers.models import WorkerProfile


class Booking(models.Model):
    """A single job request from a customer, optionally assigned to a worker."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"          # created, awaiting worker assignment/acceptance
        ACCEPTED = "accepted", "Accepted"        # worker accepted
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings_made"
    )
    worker = models.ForeignKey(
        WorkerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings"
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="bookings")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    scheduled_start = models.DateTimeField()
    notes = models.TextField(blank=True)

    estimated_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking<{self.id}> {self.category} - {self.status}"


class BookingStatusLog(models.Model):
    """Audit trail of status transitions for a booking."""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="status_logs")
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["changed_at"]

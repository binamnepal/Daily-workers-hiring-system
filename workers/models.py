import uuid
from django.conf import settings
from django.db import models

from categories.models import ServiceCategory


class WorkerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="worker_profile"
    )
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_jobs_completed = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(ServiceCategory, related_name="workers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WorkerProfile<{self.user.username}>"


class Availability(models.Model):
    """A recurring weekly time slot during which a worker is bookable."""

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name="availability_slots")
    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["weekday", "start_time"]
        constraints = [
            models.CheckConstraint(condition=models.Q(end_time__gt=models.F("start_time")), name="availability_end_after_start")
        ]

    def __str__(self):
        return f"{self.worker} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"

"""
Business logic for worker profiles: creation, availability management,
and the search/matching used when a customer wants to hire someone.
"""
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q

from categories.models import ServiceCategory

from .models import Availability, WorkerProfile


class WorkerService:

    @staticmethod
    @transaction.atomic
    def create_profile(*, user, skills, city, bio="", hourly_rate=None):
        if hasattr(user, "worker_profile"):
            raise ValidationError("This user already has a worker profile.")

        profile = WorkerProfile.objects.create(
            user=user, bio=bio, hourly_rate=hourly_rate, city=city
        )
        categories = ServiceCategory.objects.filter(slug__in=skills, is_active=True)
        if not categories.exists():
            raise ValidationError("None of the given skills match an active service category.")
        profile.skills.set(categories)
        return profile

    @staticmethod
    def add_availability(*, worker, weekday, start_time, end_time):
        if start_time >= end_time:
            raise ValidationError("start_time must be before end_time.")
        return Availability.objects.create(
            worker=worker, weekday=weekday, start_time=start_time, end_time=end_time
        )

    @staticmethod
    def set_available(worker, available: bool):
        worker.is_available = available
        worker.save(update_fields=["is_available"])
        return worker

    @staticmethod
    def search(*, category_slug=None, city=None, min_rating=None, at_datetime: datetime = None):
        """
        Core matching query for 'find me a plumber near me right now'.
        Filters on skill category, city, minimum rating, and (optionally)
        whether the worker has an availability slot covering at_datetime.
        """
        qs = WorkerProfile.objects.filter(is_available=True).select_related("user")

        if category_slug:
            qs = qs.filter(skills__slug=category_slug)
        if city:
            qs = qs.filter(city__iexact=city)
        if min_rating is not None:
            qs = qs.filter(average_rating__gte=min_rating)
        if at_datetime is not None:
            weekday = at_datetime.weekday()
            time_of_day = at_datetime.time()
            qs = qs.filter(
                availability_slots__weekday=weekday,
                availability_slots__start_time__lte=time_of_day,
                availability_slots__end_time__gte=time_of_day,
            )

        return qs.distinct().order_by("-average_rating")

    @staticmethod
    def record_completed_job(worker: WorkerProfile):
        worker.total_jobs_completed += 1
        worker.save(update_fields=["total_jobs_completed"])
        return worker

    @staticmethod
    def recalculate_rating(worker: WorkerProfile):
        """Recomputes average_rating from related reviews. Called by ReviewService."""
        from django.db.models import Avg

        from reviews.models import Review

        avg = Review.objects.filter(worker=worker).aggregate(avg=Avg("rating"))["avg"] or 0
        worker.average_rating = round(avg, 2)
        worker.save(update_fields=["average_rating"])
        return worker

from django.contrib import admin

from .models import Availability, WorkerProfile


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1


@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "is_available", "is_verified", "average_rating", "total_jobs_completed"]
    list_filter = ["is_available", "is_verified", "city", "skills"]
    filter_horizontal = ["skills"]
    inlines = [AvailabilityInline]

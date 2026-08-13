from django.contrib import admin

from .models import Booking, BookingStatusLog


class BookingStatusLogInline(admin.TabularInline):
    model = BookingStatusLog
    extra = 0
    readonly_fields = ["from_status", "to_status", "changed_at", "note"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "worker", "category", "status", "scheduled_start", "created_at"]
    list_filter = ["status", "category", "city"]
    inlines = [BookingStatusLogInline]

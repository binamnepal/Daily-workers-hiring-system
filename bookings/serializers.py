from rest_framework import serializers

from accounts.serializers import UserSerializer
from categories.serializers import ServiceCategorySerializer
from workers.serializers import WorkerProfileSerializer

from .models import Booking, BookingStatusLog


class BookingStatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatusLog
        fields = ["from_status", "to_status", "changed_at", "note"]


class BookingSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    worker = WorkerProfileSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    status_logs = BookingStatusLogSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "customer", "worker", "category", "status",
            "address", "city", "scheduled_start", "notes",
            "estimated_price", "final_price",
            "created_at", "updated_at", "completed_at",
            "cancelled_at", "cancellation_reason", "status_logs",
        ]
        read_only_fields = [
            "id", "customer", "worker", "status", "estimated_price", "final_price",
            "created_at", "updated_at", "completed_at", "cancelled_at",
        ]


class CreateBookingSerializer(serializers.Serializer):
    category_slug = serializers.SlugField()
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    scheduled_start = serializers.DateTimeField()
    notes = serializers.CharField(required=False, allow_blank=True)
    worker_id = serializers.UUIDField(required=False)


class CancelBookingSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)


class CompleteBookingSerializer(serializers.Serializer):
    final_price = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)


class AssignWorkerSerializer(serializers.Serializer):
    worker_id = serializers.UUIDField()

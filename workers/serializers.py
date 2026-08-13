from rest_framework import serializers

from accounts.serializers import UserSerializer
from categories.serializers import ServiceCategorySerializer

from .models import Availability, WorkerProfile


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["id", "weekday", "start_time", "end_time"]


class WorkerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = ServiceCategorySerializer(many=True, read_only=True)
    availability_slots = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = WorkerProfile
        fields = [
            "id", "user", "bio", "hourly_rate", "city", "is_available",
            "is_verified", "average_rating", "total_jobs_completed",
            "skills", "availability_slots",
        ]
        read_only_fields = ["id", "average_rating", "total_jobs_completed", "is_verified"]


class WorkerSearchQuerySerializer(serializers.Serializer):
    category = serializers.SlugField(required=False)
    city = serializers.CharField(required=False)
    min_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)


class AddAvailabilitySerializer(serializers.Serializer):
    weekday = serializers.IntegerField(min_value=0, max_value=6)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

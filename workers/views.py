from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WorkerProfile
from .serializers import (
    AddAvailabilitySerializer,
    WorkerProfileSerializer,
    WorkerSearchQuerySerializer,
)
from .services import WorkerService


class WorkerSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = WorkerSearchQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        workers = WorkerService.search(
            category_slug=query.validated_data.get("category"),
            city=query.validated_data.get("city"),
            min_rating=query.validated_data.get("min_rating"),
        )
        return Response(WorkerProfileSerializer(workers, many=True).data)


class WorkerDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = WorkerProfileSerializer
    queryset = WorkerProfile.objects.all()
    lookup_field = "id"


class MyWorkerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = getattr(request.user, "worker_profile", None)
        if profile is None:
            return Response({"detail": "No worker profile for this user."}, status=404)
        return Response(WorkerProfileSerializer(profile).data)


class AddAvailabilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = getattr(request.user, "worker_profile", None)
        if profile is None:
            return Response({"detail": "No worker profile for this user."}, status=404)

        serializer = AddAvailabilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            slot = WorkerService.add_availability(worker=profile, **serializer.validated_data)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(WorkerProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


class SetAvailableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = getattr(request.user, "worker_profile", None)
        if profile is None:
            return Response({"detail": "No worker profile for this user."}, status=404)
        available = bool(request.data.get("is_available", True))
        profile = WorkerService.set_available(profile, available)
        return Response(WorkerProfileSerializer(profile).data)

from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workers.models import WorkerProfile

from .models import Booking
from .serializers import (
    AssignWorkerSerializer,
    BookingSerializer,
    CancelBookingSerializer,
    CompleteBookingSerializer,
    CreateBookingSerializer,
)
from .services import BookingService


def _err(exc):
    return Response({"detail": exc.messages if hasattr(exc, "messages") else str(exc)},
                     status=status.HTTP_400_BAD_REQUEST)


class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = BookingService.create_booking(customer=request.user, **serializer.validated_data)
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, "worker_profile"):
            bookings = BookingService.list_for_worker(request.user.worker_profile)
        else:
            bookings = BookingService.list_for_customer(request.user)
        return Response(BookingSerializer(bookings, many=True).data)


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        return Response(BookingSerializer(booking).data)


class AssignWorkerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id, customer=request.user)
        serializer = AssignWorkerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        worker = get_object_or_404(WorkerProfile, id=serializer.validated_data["worker_id"])
        try:
            booking = BookingService.assign_worker(booking=booking, worker=worker)
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data)


class AcceptBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        try:
            booking = BookingService.accept(booking=booking, worker=request.user.worker_profile)
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data)


class RejectBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        reason = request.data.get("reason", "")
        try:
            booking = BookingService.reject(booking=booking, worker=request.user.worker_profile, reason=reason)
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data)


class StartBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        try:
            booking = BookingService.start(booking=booking, worker=request.user.worker_profile)
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data)


class CompleteBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        serializer = CompleteBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = BookingService.complete(
                booking=booking, worker=request.user.worker_profile,
                final_price=serializer.validated_data.get("final_price"),
            )
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data)


class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        booking = get_object_or_404(Booking, id=id)
        serializer = CancelBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = BookingService.cancel(
                booking=booking, actor=request.user, reason=serializer.validated_data.get("reason", "")
            )
        except DjangoValidationError as exc:
            return _err(exc)
        return Response(BookingSerializer(booking).data)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404, redirect, render

from workers.models import WorkerProfile

from .forms import AssignWorkerForm, CancelBookingForm, CompleteBookingForm, CreateBookingForm
from .models import Booking
from .services import BookingService


@login_required
def create_booking(request):
    if request.method == "POST":
        form = CreateBookingForm(request.POST)
        if form.is_valid():
            try:
                booking = BookingService.create_booking(customer=request.user, **form.cleaned_data)
            except DjangoValidationError as exc:
                form.add_error(None, exc.message if hasattr(exc, "message") else str(exc))
            else:
                messages.success(request, "Booking request created.")
                return redirect("bookings:detail", id=booking.id)
    else:
        initial = {}
        worker_id = request.GET.get("worker_id")
        if worker_id:
            initial["worker_id"] = worker_id
        form = CreateBookingForm(initial=initial)
    return render(request, "bookings/create.html", {"form": form})


@login_required
def my_bookings(request):
    if hasattr(request.user, "worker_profile"):
        bookings = BookingService.list_for_worker(request.user.worker_profile)
    else:
        bookings = BookingService.list_for_customer(request.user)
    return render(request, "bookings/mine.html", {"bookings": bookings})


@login_required
def booking_detail(request, id):
    booking = get_object_or_404(Booking, id=id)
    return render(request, "bookings/detail.html", {
        "booking": booking,
        "assign_form": AssignWorkerForm(),
        "cancel_form": CancelBookingForm(),
        "complete_form": CompleteBookingForm(),
    })


@login_required
def assign_worker(request, id):
    booking = get_object_or_404(Booking, id=id, customer=request.user)
    if request.method == "POST":
        form = AssignWorkerForm(request.POST)
        if form.is_valid():
            worker = get_object_or_404(WorkerProfile, id=form.cleaned_data["worker_id"])
            try:
                BookingService.assign_worker(booking=booking, worker=worker)
                messages.success(request, "Worker assigned.")
            except DjangoValidationError as exc:
                messages.error(request, str(exc))
    return redirect("bookings:detail", id=id)


def _worker_action(request, id, action, **kwargs):
    booking = get_object_or_404(Booking, id=id)
    worker = getattr(request.user, "worker_profile", None)
    if worker is None:
        messages.error(request, "You don't have a worker profile.")
        return redirect("bookings:detail", id=id)
    try:
        action(booking=booking, worker=worker, **kwargs)
        messages.success(request, "Booking updated.")
    except DjangoValidationError as exc:
        messages.error(request, str(exc))
    return redirect("bookings:detail", id=id)


@login_required
def accept_booking(request, id):
    return _worker_action(request, id, BookingService.accept)


@login_required
def reject_booking(request, id):
    form = CancelBookingForm(request.POST or None)
    reason = form.data.get("reason", "") if request.method == "POST" else ""
    return _worker_action(request, id, BookingService.reject, reason=reason)


@login_required
def start_booking(request, id):
    return _worker_action(request, id, BookingService.start)


@login_required
def complete_booking(request, id):
    form = CompleteBookingForm(request.POST or None)
    final_price = None
    if form.is_valid():
        final_price = form.cleaned_data.get("final_price")
    return _worker_action(request, id, BookingService.complete, final_price=final_price)


@login_required
def cancel_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    reason = request.POST.get("reason", "")
    try:
        BookingService.cancel(booking=booking, actor=request.user, reason=reason)
        messages.success(request, "Booking cancelled.")
    except DjangoValidationError as exc:
        messages.error(request, str(exc))
    return redirect("bookings:detail", id=id)

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import redirect, render

from bookings.models import Booking
from workers.models import WorkerProfile

from .forms import (
    CustomerRegisterForm,
    LocationUpdateForm,
    LoginForm,
    WorkerRegisterForm,
)
from .services import AccountService


def register_customer(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)

        if form.is_valid():
            try:
                user = AccountService.register_customer(**form.cleaned_data)
            except DjangoValidationError as exc:
                form.add_error(
                    None,
                    exc.message if hasattr(exc, "message") else str(exc),
                )
            else:
                login(request, user)
                messages.success(
                    request,
                    "Welcome! Your customer account has been created.",
                )
                return redirect("accounts:dashboard")
    else:
        form = CustomerRegisterForm()

    return render(request, "accounts/register_customer.html", {"form": form})


def register_worker(request):
    if request.method == "POST":
        form = WorkerRegisterForm(request.POST)

        if form.is_valid():
            try:
                user = AccountService.register_worker(**form.cleaned_data)
            except DjangoValidationError as exc:
                form.add_error(
                    None,
                    exc.message if hasattr(exc, "message") else str(exc),
                )
            else:
                login(request, user)
                messages.success(
                    request,
                    "Welcome! Your worker profile has been created.",
                )
                return redirect("accounts:dashboard")
    else:
        form = WorkerRegisterForm()

    return render(request, "accounts/register_worker.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user is not None:
                login(request, user)
                return redirect("accounts:dashboard")

            form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def dashboard(request):
    """Entry point after login — routes to the correct dashboard."""
    if request.user.is_worker:
        return redirect("accounts:worker_dashboard")
    return redirect("accounts:customer_dashboard")


@login_required
def customer_dashboard(request):
    user_bookings = Booking.objects.filter(customer=request.user)

    context = {
        "total_bookings": user_bookings.count(),
        "pending_bookings": user_bookings.filter(
            status=Booking.Status.PENDING
        ).count(),
        "completed_bookings": user_bookings.filter(
            status=Booking.Status.COMPLETED
        ).count(),
        "cancelled_bookings": user_bookings.filter(
            status=Booking.Status.CANCELLED
        ).count(),
        "recent_bookings": user_bookings[:5],
    }

    return render(request, "accounts/customer_dashboard.html", context)


@login_required
def worker_dashboard(request):
    try:
        worker_profile = WorkerProfile.objects.get(user=request.user)
    except WorkerProfile.DoesNotExist:
        messages.error(request, "No worker profile found for this account.")
        return redirect("accounts:dashboard")

    assigned_bookings = Booking.objects.filter(worker=worker_profile)

    context = {
        "total_bookings": assigned_bookings.count(),
        "pending_bookings": assigned_bookings.filter(
            status=Booking.Status.PENDING
        ).count(),
        "completed_bookings": assigned_bookings.filter(
            status=Booking.Status.COMPLETED
        ).count(),
        "cancelled_bookings": assigned_bookings.filter(
            status=Booking.Status.CANCELLED
        ).count(),
        "recent_bookings": assigned_bookings[:5],
    }

    return render(request, "accounts/worker_dashboard.html", context)


@login_required
def update_location(request):
    if request.method == "POST":
        form = LocationUpdateForm(request.POST)

        if form.is_valid():
            AccountService.update_location(user=request.user, **form.cleaned_data)
            messages.success(request, "Location updated.")
            return redirect("accounts:dashboard")
    else:
        form = LocationUpdateForm(
            initial={
                "latitude": request.user.latitude,
                "longitude": request.user.longitude,
                "address": request.user.address,
            }
        )

    return render(request, "accounts/update_location.html", {"form": form})


def register_chooser(request):
    return render(request, "accounts/register.html")
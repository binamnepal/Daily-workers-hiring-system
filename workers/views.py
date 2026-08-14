from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvailabilityForm, WorkerSearchForm
from .models import WorkerProfile
from .services import WorkerService


def worker_search(request):
    form = WorkerSearchForm(request.GET or None)
    workers = []
    if form.is_valid():
        workers = WorkerService.search(
            category_slug=form.cleaned_data.get("category") or None,
            city=form.cleaned_data.get("city") or None,
            min_rating=form.cleaned_data.get("min_rating"),
        )
    return render(request, "workers/search.html", {"form": form, "workers": workers})


def worker_detail(request, id):
    worker = get_object_or_404(WorkerProfile, id=id)
    return render(request, "workers/detail.html", {"worker": worker})


@login_required
def my_profile(request):
    profile = getattr(request.user, "worker_profile", None)
    if profile is None:
        messages.error(request, "You don't have a worker profile.")
        return redirect("accounts:dashboard")

    if request.method == "POST" and "toggle_available" in request.POST:
        WorkerService.set_available(profile, not profile.is_available)
        return redirect("workers:my_profile")

    availability_form = AvailabilityForm()
    return render(request, "workers/my_profile.html", {"worker": profile, "form": availability_form})


@login_required
def add_availability(request):
    profile = getattr(request.user, "worker_profile", None)
    if profile is None:
        messages.error(request, "You don't have a worker profile.")
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            try:
                WorkerService.add_availability(
                    worker=profile,
                    weekday=int(form.cleaned_data["weekday"]),
                    start_time=form.cleaned_data["start_time"],
                    end_time=form.cleaned_data["end_time"],
                )
            except DjangoValidationError as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, "Availability slot added.")
    return redirect("workers:my_profile")
def search(request):
    query = request.GET.get("q", "")

    workers = Worker.objects.all()

    if query:
        workers = workers.filter(
            user__username__icontains=query
        )

    return render(
        request,
        "workers/search.html",
        {
            "workers": workers,
            "query": query,
        },
    )
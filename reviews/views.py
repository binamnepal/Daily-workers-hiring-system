from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from workers.models import WorkerProfile

from .forms import CreateReviewForm
from .services import ReviewService


@login_required
def create_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            try:
                ReviewService.create_review(
                    booking=booking,
                    customer=request.user,
                    rating=int(form.cleaned_data["rating"]),
                    comment=form.cleaned_data["comment"],
                )
            except DjangoValidationError as exc:
                messages.error(request, str(exc))
            else:
                messages.success(request, "Thanks for your review!")
                return redirect("bookings:detail", id=booking.id)
    else:
        form = CreateReviewForm()
    return render(request, "reviews/create.html", {"form": form, "booking": booking})


def worker_reviews(request, worker_id):
    worker = get_object_or_404(WorkerProfile, id=worker_id)
    reviews = ReviewService.list_for_worker(worker)
    return render(request, "reviews/list.html", {"worker": worker, "reviews": reviews})

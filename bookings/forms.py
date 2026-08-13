from django import forms

from categories.models import ServiceCategory


class CreateBookingForm(forms.Form):
    category_slug = forms.ChoiceField(label="Service")
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    scheduled_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    notes = forms.CharField(widget=forms.Textarea, required=False)
    worker_id = forms.UUIDField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_slug"].choices = [
            (c.slug, c.name) for c in ServiceCategory.objects.filter(is_active=True)
        ]


class CancelBookingForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, required=False)


class CompleteBookingForm(forms.Form):
    final_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)


class AssignWorkerForm(forms.Form):
    worker_id = forms.UUIDField(widget=forms.HiddenInput)

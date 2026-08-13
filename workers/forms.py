from django import forms

from categories.models import ServiceCategory


class WorkerSearchForm(forms.Form):
    category = forms.ChoiceField(required=False)
    city = forms.CharField(max_length=100, required=False)
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [("", "Any")] + [
            (c.slug, c.name) for c in ServiceCategory.objects.filter(is_active=True)
        ]


class AvailabilityForm(forms.Form):
    WEEKDAY_CHOICES = [
        (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"),
        (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
    ]
    weekday = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

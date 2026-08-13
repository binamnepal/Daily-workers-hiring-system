from django import forms


class CustomerRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)


class WorkerRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    phone_number = forms.CharField(max_length=20)
    city = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    hourly_rate = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    skills = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from categories.models import ServiceCategory
        self.fields["skills"].choices = [
            (c.slug, c.name) for c in ServiceCategory.objects.filter(is_active=True)
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class LocationUpdateForm(forms.Form):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6)
    address = forms.CharField(max_length=255, required=False)

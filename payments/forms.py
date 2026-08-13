from django import forms

from .models import Payment


class CreatePaymentForm(forms.Form):
    method = forms.ChoiceField(choices=Payment.Method.choices, initial=Payment.Method.CASH)


class ChargePaymentForm(forms.Form):
    provider_reference = forms.CharField(max_length=255, required=False)

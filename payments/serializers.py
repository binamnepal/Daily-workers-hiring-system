from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "booking", "amount", "method", "status", "provider_reference", "created_at", "paid_at"]
        read_only_fields = ["id", "amount", "status", "created_at", "paid_at"]


class CreatePaymentSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=Payment.Method.choices, default=Payment.Method.CASH)


class ChargePaymentSerializer(serializers.Serializer):
    provider_reference = serializers.CharField(required=False, allow_blank=True)

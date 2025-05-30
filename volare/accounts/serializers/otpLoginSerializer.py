from django.db.models import Q
from rest_framework import serializers
from ..models.account import Account


class RequestOTPSerializer(serializers.Serializer):
    phonenumber_or_email = serializers.CharField(required=True)

    def validate_phonenumber_or_email(self, value):
        try:
            user = Account.objects.get(Q(email=value) | Q(phone_number=value))
        except Account.DoesNotExist:
            raise serializers.ValidationError("User not found")

        self.context['user'] = user
        return value


class VerifyOTPSerializer(serializers.Serializer):
    value = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        value = data.get('value')
        otp = data.get('otp')

        if not value or not otp:
            raise serializers.ValidationError("Both value and OTP are required.")

        try:
            user = Account.objects.get(Q(email=value) | Q(phone_number=value))
        except Account.DoesNotExist:
            raise serializers.ValidationError("No account found with that email or phone number.")

        # Attach user to validated data so view can access it
        data['user'] = user
        return data

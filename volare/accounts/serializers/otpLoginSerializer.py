from django.db.models import Q
from rest_framework import serializers
from ..models.account import Account


class RequestOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)

    def validate_identifier(self, value):
        try:
            user = Account.objects.get(Q(email=value) | Q(phone_number=value))
        except Account.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        self.context['user'] = user
        return value


class VerifyOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        identifier = data.get('identifier')
        otp = data.get('otp')

        if not identifier or not otp:
            raise serializers.ValidationError("Both identifier and OTP are required.")

        try:
            user = Account.objects.get(Q(email=identifier) | Q(phone_number=identifier))
        except Account.DoesNotExist:
            raise serializers.ValidationError("No account found with that identifier.")

        data['user'] = user
        return data

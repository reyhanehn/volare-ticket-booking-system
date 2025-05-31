from rest_framework import serializers
from django.db.models import Q
from ..Models.account import Account  # adjust import as needed
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RequestForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        try:
            user = Account.objects.get(Q(email=value) | Q(phone_number=value))
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account not found.")
        self.context['user'] = user
        return value


class VerifyForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        value = data.get("identifier")

        try:
            user = Account.objects.get(Q(email=value) | Q(phone_number=value))
        except Account.DoesNotExist:
            raise serializers.ValidationError("No matching account.")

        data["user"] = user
        return data

from rest_framework import serializers
from ..models.account import Account
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import connection


class RequestForgotPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM account
                WHERE email = %s OR phone_number = %s
                LIMIT 1
            """, [value, value])
            row = cursor.fetchone()

        if not row:
            raise serializers.ValidationError("Account not found.")

        # Get field indices from model meta
        columns = [col[0] for col in cursor.description]
        data = dict(zip(columns, row))
        user = Account(**data)
        user._state.adding = False

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

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM account
                WHERE email = %s OR phone_number = %s
                LIMIT 1
            """, [value, value])
            row = cursor.fetchone()

        if not row:
            raise serializers.ValidationError("No matching account.")

        columns = [col[0] for col in cursor.description]
        user_data = dict(zip(columns, row))
        user = Account(**user_data)
        user._state.adding = False

        data["user"] = user
        return data

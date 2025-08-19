from django.db import connection
from rest_framework import serializers
from ..models.account import Account


class RequestOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)

    def validate_identifier(self, value):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM account
                WHERE email = %s OR phone_number = %s
                LIMIT 1
            """, [value, value])
            row = cursor.fetchone()

            if not row:
                raise serializers.ValidationError("User not found.")

            # Safe use of cursor.description
            if cursor.description is None:
                raise serializers.ValidationError("Database error: no column info available.")

            columns = [col[0] for col in cursor.description]
            user_data = dict(zip(columns, row))
            user = Account(**user_data)
            user._state.adding = False

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

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM account
                WHERE email = %s OR phone_number = %s
                LIMIT 1
            """, [identifier, identifier])
            row = cursor.fetchone()

            if not row:
                raise serializers.ValidationError("No account found with that identifier.")

            if cursor.description is None:
                raise serializers.ValidationError("Database error: no column info available.")

            columns = [col[0] for col in cursor.description]
            user_data = dict(zip(columns, row))
            user = Account(**user_data)
            user._state.adding = False

            data['user'] = user
        return data

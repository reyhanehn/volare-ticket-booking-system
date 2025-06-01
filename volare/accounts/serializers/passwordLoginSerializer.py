from django.db.models import Q
from rest_framework import serializers
from ..models.account import Account

class PasswordLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # replaces "value"
    password = serializers.CharField()

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        try:
            user = Account.objects.get(Q(email=identifier) | Q(phone_number=identifier))
        except Account.DoesNotExist:
            raise serializers.ValidationError("No account found with this email or phone number.")

        # Attach user to validated data
        data['user'] = user
        return data
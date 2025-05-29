from rest_framework import serializers
from ..Models.account import Account
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class AccountSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone_number', 'email', 'name', 'lastname', 'password_hash', 'role']
        extra_kwargs = {
            'password_hash': {'write_only': True},
            'role': {'required': False},
        }

    def validate_password_hash(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        validated_data['password_hash'] = make_password(validated_data['password_hash'])
        if 'role' not in validated_data:
            validated_data['role'] = 'Customer'
        return Account.objects.create(**validated_data)

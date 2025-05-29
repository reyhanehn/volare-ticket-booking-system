from rest_framework import serializers
from ..Models.account import Account
from django.contrib.auth.hashers import make_password


class AccountSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone_number', 'email', 'name', 'lastname', 'password_hash', 'role']
        extra_kwargs = {
            'password_hash': {'write_only': True},
            'role': {'required': False},
        }

    def create(self, validated_data):
        validated_data['password_hash'] = make_password(validated_data['password_hash'])
        if 'role' not in validated_data:
            validated_data['role'] = 'Customer'
        return Account.objects.create(**validated_data)

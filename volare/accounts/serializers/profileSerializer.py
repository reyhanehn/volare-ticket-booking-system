# accounts/serializers/profileSerializer.py

from rest_framework import serializers
from ..models.account import Account  # or from django.contrib.auth.models if using default User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account  # use your custom Account model here
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['id']


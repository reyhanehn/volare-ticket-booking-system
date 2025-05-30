from rest_framework import serializers
from ..models.account import Account
from django.contrib.auth.hashers import make_password
from django.db import connection


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
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO account (phone_number, email, name, lastname, password_hash, role, status, registration_date, is_staff, is_superuser)
                VALUES (%s, %s, %s, %s, %s, %s, 'Active', CURRENT_DATE, false, false)
                RETURNING account_id, registration_date;
            """, [
                validated_data.get('phone_number'),
                validated_data.get('email'),
                validated_data.get('name'),
                validated_data.get('lastname'),
                validated_data.get('password_hash'),
                validated_data.get('role')
            ])
            row = cursor.fetchone()
            account_id = row[0]
            cursor.execute("""
                INSERT INTO wallet(account_id, balance)
                VALUES (%s, 0.0);
            """, [
                account_id
            ])
        account = Account(
            account_id=row[0],
            phone_number=validated_data.get('phone_number'),
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            lastname=validated_data.get('lastname'),
            password_hash=validated_data.get('password_hash'),
            role=validated_data.get('role'),
            status="Active",
            registration_date=row[1],
        )

        account._state.adding = False  # Mark instance as retrieved, not new
        return account

import re
from datetime import date, timedelta
from django.db import connection
from rest_framework import serializers
from ..models.account import Account
# from volare.bookings.models.location import Location


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    city = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Account
        exclude = ('account_id', 'password_hash', 'is_superuser', 'is_staff', 'groups', 'user_permissions')
        read_only_fields = ('role', 'status', 'registration_date', 'last_login','is_superuser', 'is_staff', 'groups', 'user_permissions')

    def validate(self, data):
        user = self.instance

        email = data.get('email', getattr(user, 'email', None))
        phone_number = data.get('phone_number', getattr(user, 'phone_number', None))
        name = data.get('name', getattr(user, 'name', None))
        lastname = data.get('lastname', getattr(user, 'lastname', None))
        birthdate = data.get('birth_date', getattr(user, 'birth_date', None))
        city_id = data.get('city', getattr(user.city, 'pk', None) if user.city else None)

        if email:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM account WHERE email = %s AND account_id != %s",
                    [email, user.account_id]
                )
                if cursor.fetchone():
                    raise serializers.ValidationError({"email": "This email is already in use."})

        if phone_number:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM account WHERE phone_number = %s AND account_id != %s",
                    [phone_number, user.account_id]
                )
                if cursor.fetchone():
                    raise serializers.ValidationError({"phone_number": "This phone number is already in use."})

        if not email and not phone_number:
            raise serializers.ValidationError(
                "Either email or phone number must be provided."
            )

        name_pattern = re.compile(r'^[A-Za-z]+(\s[A-Za-z]+)*$')
        if name and not name_pattern.match(name):
            raise serializers.ValidationError({"name": "Invalid name format."})
        if lastname and not name_pattern.match(lastname):
            raise serializers.ValidationError({"lastname": "Invalid lastname format."})

        if birthdate:
            if birthdate > date.today():
                raise serializers.ValidationError({"birthdate": "Birthdate cannot be in the future."})
            min_birthdate = date.today() - timedelta(days=15 * 365)  # approx 15 years
            if birthdate > min_birthdate:
                raise serializers.ValidationError({"birthdate": "You must be at least 15 years old."})

        if city_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM location WHERE location_id = %s",
                    [city_id]
                )
                if cursor.fetchone() is None:
                    raise serializers.ValidationError({"city": "City with this ID does not exist."})

        for field in ['role', 'status', 'registration_date']:
            if field in data and getattr(user, field) != data[field]:
                raise serializers.ValidationError({field: f"{field} is read-only and cannot be changed."})

        return data

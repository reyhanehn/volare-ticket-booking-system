import re
from datetime import date, timedelta
from django.db import connection
from rest_framework import serializers
from ..models.account import Account


class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField(required=False)
    lastname = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    city = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Account
        exclude = ('account_id', 'password_hash', 'is_superuser', 'is_staff', 'groups', 'user_permissions')
        read_only_fields = ('role', 'status', 'registration_date', 'last_login','is_superuser', 'is_staff', 'groups', 'user_permissions')

    def validate(self, data):
        user = self.instance
        account_id = user.account_id

        email = data.get("email", user.email)
        phone_number = data.get("phone_number", user.phone_number)
        name = data.get("name", user.name)
        lastname = data.get("lastname", user.lastname)
        birthdate = data.get("birth_date", user.birth_date)
        city_id = data.get("city", user.city_id if user.city else None)

        if not email and not phone_number:
            raise serializers.ValidationError("Either email or phone number must be provided.")

        with connection.cursor() as cursor:
            if email:
                cursor.execute("SELECT 1 FROM account WHERE email = %s AND account_id != %s", [email, account_id])
                if cursor.fetchone():
                    raise serializers.ValidationError({"email": "This email is already in use."})

            if phone_number:
                cursor.execute("SELECT 1 FROM account WHERE phone_number = %s AND account_id != %s", [phone_number, account_id])
                if cursor.fetchone():
                    raise serializers.ValidationError({"phone_number": "This phone number is already in use."})
                phone_pattern = re.compile(r'^09\d{9}$')
                if not phone_pattern.match(phone_number):
                    raise serializers.ValidationError(
                        {"phone_number": "Invalid Iranian phone number format. Must be 11 digits and start with 09."})

            if city_id is not None:
                cursor.execute("SELECT 1 FROM bookings_location WHERE location_id = %s", [city_id])
                if not cursor.fetchone():
                    raise serializers.ValidationError({"city": "City with this ID does not exist."})

        name_pattern = re.compile(r'^[A-Za-z]+(\s[A-Za-z]+)*$')
        if name and not name_pattern.match(name):
            raise serializers.ValidationError({"name": "Invalid name format."})
        if lastname and not name_pattern.match(lastname):
            raise serializers.ValidationError({"lastname": "Invalid lastname format."})

        if birthdate:
            if birthdate > date.today():
                raise serializers.ValidationError({"birth_date": "Birthdate cannot be in the future."})
            if birthdate > (date.today() - timedelta(days=15 * 365)):
                raise serializers.ValidationError({"birth_date": "You must be at least 15 years old."})

        if city_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM bookings_location WHERE location_id = %s",
                    [city_id]
                )
                if cursor.fetchone() is None:
                    raise serializers.ValidationError({"city": "City with this ID does not exist."})

        for field in ['role', 'status', 'registration_date']:
            if field in data and getattr(user, field) != data[field]:
                raise serializers.ValidationError({field: f"{field} is read-only and cannot be changed."})

        return data

    def update(self, instance, validated_data):
        account_id = instance.account_id

        columns = []
        values = []

        field_map = {
            "email": "email",
            "phone_number": "phone_number",
            "name": "name",
            "lastname": "lastname",
            "birth_date": "birth_date",
            "city": "city_id"
        }

        for field, column in field_map.items():
            if field in validated_data:
                columns.append(f"{column} = %s")
                values.append(validated_data[field])

        if columns:
            set_clause = ", ".join(columns)
            with connection.cursor() as cursor:
                cursor.execute(
                    f"UPDATE account SET {set_clause} WHERE account_id = %s",
                    values + [account_id]
                )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.account_id, a.name, a.lastname, a.email, a.phone_number,
                       a.role, a.status, a.registration_date, a.birth_date,
                       l.city
                FROM account a
                LEFT JOIN bookings_location l ON a.city_id = l.location_id
                WHERE a.account_id = %s
            """, [account_id])
            row = cursor.fetchone()

        if not row:
            raise serializers.ValidationError("Failed to retrieve updated profile.")

        return {
            "account_id": row[0],
            "name": row[1],
            "lastname": row[2],
            "email": row[3],
            "phone_number": row[4],
            "role": row[5],
            "status": row[6],
            "registration_date": row[7],
            "birth_date": row[8],
            "city": row[9]
        }

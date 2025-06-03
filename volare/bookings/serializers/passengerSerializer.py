from rest_framework import serializers
from django.db import connection
from datetime import date


class CreatePassengerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    ssn = serializers.CharField(max_length=10)
    birthdate = serializers.DateField()
    picture_url = serializers.CharField(required=False, allow_blank=True)

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Name must contain only letters.")
        return value

    def validate_lastname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Lastname must contain only letters.")
        return value

    def validate_ssn(self, value):
        if value and len(value) != 10:
            raise serializers.ValidationError("SSN must be 10 digits.")
        return value

    def validate_birthdate(self, value):
        if value > date.today():
            raise serializers.ValidationError("Birthdate cannot be in the future.")
        return value

    def create(self, validated_data):
        account_id = self.context['request'].user.account_id

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO bookings_passenger (name, lastname, ssn, birthdate, picture_url, related_account_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING passenger_id;
            """, [
                validated_data.get("name"),
                validated_data.get("lastname"),
                validated_data.get("ssn"),
                validated_data.get("birthdate"),
                validated_data.get("picture_url"),
                account_id
            ])
            passenger_id = cursor.fetchone()[0]

        return {
            "passenger_id": passenger_id,
            **validated_data
        }


class PassengerListSerializer(serializers.Serializer):
    passenger_id = serializers.IntegerField()
    name = serializers.CharField()
    lastname = serializers.CharField()
    ssn = serializers.CharField()
    birthdate = serializers.DateField()
    picture_url = serializers.CharField(allow_null=True)

    @classmethod
    def get_passengers(cls, account_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT passenger_id, name, lastname, ssn, birthdate, picture_url
                FROM bookings_passenger
                WHERE related_account_id = %s
            """, [account_id])
            rows = cursor.fetchall()

        # Manually map SQL rows to dicts
        passengers = [
            {
                "passenger_id": row[0],
                "name": row[1],
                "lastname": row[2],
                "ssn": row[3],
                "birthdate": row[4],
                "picture_url": row[5],
            }
            for row in rows
        ]
        return cls(passengers, many=True).data

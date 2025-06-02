from rest_framework import serializers
from django.db import connection
import re

class LocationSerializer(serializers.Serializer):
    country = serializers.CharField()
    city = serializers.CharField()

    def validate_country(self, value):
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)*$', value):
            raise serializers.ValidationError("Country name must contain only letters and spaces.")
        return value

    def validate_city(self, value):
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)*$', value):
            raise serializers.ValidationError("City name must contain only letters and spaces.")
        return value

    def validate(self, data):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM bookings_location WHERE LOWER(country) = LOWER(%s) AND LOWER(city) = LOWER(%s)",
                [data['country'], data['city']]
            )
            if cursor.fetchone():
                raise serializers.ValidationError("This location already exists.")
        return data

    def create(self, validated_data):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO bookings_location (country, city) VALUES (%s, %s) RETURNING country, city",
                [validated_data['country'], validated_data['city']]
            )
            country, city = cursor.fetchone()
        return {"country": country, "city": city}

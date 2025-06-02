from rest_framework import serializers
from django.db import connection
import re

class StationSerializer(serializers.Serializer):
    station_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    type = serializers.CharField()
    location = serializers.IntegerField()  # This refers to `location_id`

    def validate_name(self, value):
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+)*$', value):
            raise serializers.ValidationError("Station name must contain only letters and spaces.")
        return value

    def validate_location(self, value):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM bookings_location WHERE location_id = %s", [value])
            if not cursor.fetchone():
                raise serializers.ValidationError("Provided location_id does not exist.")
        return value

    def create(self, validated_data):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO bookings_station (name, type, location_id)
                VALUES (%s, %s, %s)
                RETURNING station_id, name, type, location_id
                """,
                [validated_data['name'], validated_data['type'], validated_data['location']]
            )
            station_id, name, type_, location_id = cursor.fetchone()
        return {
            "station_id": station_id,
            "name": name,
            "type": type_,
            "location": location_id
        }

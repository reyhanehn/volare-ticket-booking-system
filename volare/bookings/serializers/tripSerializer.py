from django.utils import timezone
from rest_framework import serializers
from django.utils.dateparse import parse_datetime
from django.db import connection
from datetime import datetime, timedelta


class TripCreateSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
    route_id = serializers.IntegerField()
    departure_datetime = serializers.DateTimeField()
    duration = serializers.DurationField()
    ticket_info = serializers.ListField(child=serializers.DictField())


    def validate(self, data):
        vehicle_id = data["vehicle_id"]
        route_id = data["route_id"]
        user_account_id = self.context["request"].user.account_id
        ticket_info = data["ticket_info"]
        departure = data["departure_datetime"]

        if departure < timezone.now() + timedelta(days=7):
            raise serializers.ValidationError("Departure must be at least one week from now.")

        with connection.cursor() as cursor:
            # Check vehicle ownership and type
            cursor.execute("""
                SELECT c.owner_id, v.type
                FROM companies_vehicle v
                JOIN companies_company c ON v.company_id = c.company_id
                WHERE v.vehicle_id = %s
            """, [vehicle_id])
            row = cursor.fetchone()
            if not row:
                raise serializers.ValidationError("Vehicle does not exist.")
            owner_id, transport_type = row
            if owner_id != user_account_id:
                raise serializers.ValidationError("You do not own this vehicle.")

            # Validate route existence
            cursor.execute("SELECT 1 FROM bookings_route WHERE route_id = %s", [route_id])
            if not cursor.fetchone():
                raise serializers.ValidationError("Route does not exist.")

            # Validate vehicle sections
            cursor.execute("""
                SELECT section_id, seats_count
                FROM companies_vehiclesection
                WHERE vehicle_id = %s
            """, [vehicle_id])
            vehicle_sections = cursor.fetchall()
            section_ids_in_vehicle = {s[0] for s in vehicle_sections}
            section_ids_in_request = {t["section_id"] for t in ticket_info}

            if len(vehicle_sections) != len(ticket_info):
                raise serializers.ValidationError("Number of tickets must match number of vehicle sections.")
            if section_ids_in_vehicle != section_ids_in_request:
                raise serializers.ValidationError("Section IDs in tickets must match the vehicle’s sections exactly.")

            # Validate station type compatibility
            expected_station_type = {
                "Train": "Train_Station",
                "Bus": "Bus_Station",
                "Airplane": "Airport"
            }.get(transport_type)

            cursor.execute("""
                SELECT s.type
                FROM bookings_station s
                JOIN bookings_route r ON r.origin_station_id = s.station_id
                WHERE r.route_id = %s
            """, [route_id])
            row = cursor.fetchone()
            if not row:
                raise serializers.ValidationError("Not a valid route.")
            station_type = row[0]
            if station_type != expected_station_type:
                raise serializers.ValidationError({
                    "origin_station": f"{transport_type} must use {expected_station_type}, but got {station_type}."
                })

        return data

    def create(self, validated_data):
        vehicle_id = validated_data["vehicle_id"]
        route_id = validated_data["route_id"]
        departure = validated_data["departure_datetime"]
        duration = validated_data["duration"]
        ticket_info = validated_data["ticket_info"]

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO bookings_trip (vehicle_id, route_id, departure_datetime, duration)
                VALUES (%s, %s, %s, %s)
                RETURNING trip_id
            """, [vehicle_id, route_id, departure, duration])
            trip_id = cursor.fetchone()[0]

            total_capacity = 0

            for ticket in ticket_info:
                section_id = ticket["section_id"]
                price = ticket["price"]

                cursor.execute("""
                    SELECT seats_count
                    FROM companies_vehiclesection
                    WHERE section_id = %s
                """, [section_id])
                seats = cursor.fetchone()[0]

                total_capacity += seats
                cursor.execute("""
                    INSERT INTO bookings_ticket (
                        trip_id, section_id, price,
                        remaining_seats, seat_start_number, seat_end_number
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, [
                    trip_id, section_id, price,
                    seats, 1, seats
                ])

        return {"trip_id": trip_id, "total_capacity": total_capacity}

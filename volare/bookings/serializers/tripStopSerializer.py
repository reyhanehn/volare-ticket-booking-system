from rest_framework import serializers
from django.db import connection
from ..models.ticket import StopType


class TripStopCreateSerializer(serializers.Serializer):
    stops = serializers.ListField(
        child=serializers.DictField(), allow_empty=False
    )

    def validate(self, data):
        trip_id = self.context["trip_id"]
        stops = data["stops"]

        with connection.cursor() as cursor:
            # ✅ Ensure trip exists
            cursor.execute("SELECT vehicle_id FROM bookings_trip WHERE trip_id = %s", [trip_id])
            trip_row = cursor.fetchone()
            if not trip_row:
                raise serializers.ValidationError("Trip does not exist.")
            vehicle_id = trip_row[0]

            # ✅ Get vehicle type
            cursor.execute("SELECT type FROM companies_vehicle WHERE vehicle_id = %s", [vehicle_id])
            vehicle_row = cursor.fetchone()
            if not vehicle_row:
                raise serializers.ValidationError("Vehicle not found.")
            vehicle_type = vehicle_row[0]  # 'Airplane', 'Train', 'Bus'

            # ✅ Allowed stop types per vehicle
            allowed_by_type = {
                "Airplane": {"Layover"},
                "Train": {"Transit", "Refuel"},
                "Bus": {"Meal", "Refuel", "Transit"}
            }
            allowed_stops = allowed_by_type.get(vehicle_type)

            existing_orders = set()
            for stop in stops:
                stop_order = stop.get("stop_order")
                stop_type = stop.get("stop_type")
                station_id = stop.get("station_id")

                # 🚨 Validate stop_order uniqueness in payload
                if stop_order in existing_orders:
                    raise serializers.ValidationError(f"Duplicate stop_order: {stop_order}")
                existing_orders.add(stop_order)

                # 🚨 Validate stop_order uniqueness in DB
                cursor.execute("""
                    SELECT 1 FROM bookings_tripstop
                    WHERE trip_id = %s AND stop_order = %s
                """, [trip_id, stop_order])
                if cursor.fetchone():
                    raise serializers.ValidationError(f"stop_order {stop_order} already exists for this trip.")

                # 🚨 Validate stop_type
                if stop_type not in StopType.values:
                    raise serializers.ValidationError(f"Invalid stop_type: {stop_type}")
                if stop_type not in allowed_stops:
                    raise serializers.ValidationError(
                        f"{stop_type} is not allowed for vehicle type '{vehicle_type}'."
                    )

                # 🚨 Validate station if not null
                if station_id is not None:
                    cursor.execute("SELECT 1 FROM bookings_station WHERE station_id = %s", [station_id])
                    if not cursor.fetchone():
                        raise serializers.ValidationError(f"Station with ID {station_id} does not exist.")

        return data

    def create(self, validated_data):
        trip_id = self.context["trip_id"]
        stops = validated_data["stops"]

        with connection.cursor() as cursor:
            for stop in stops:
                cursor.execute("""
                    INSERT INTO bookings_tripstop (
                        trip_id, stop_order, stop_type, station_id, duration
                    ) VALUES (%s, %s, %s, %s, %s)
                """, [
                    trip_id,
                    stop["stop_order"],
                    stop["stop_type"],
                    stop.get("station_id"),
                    stop.get("duration")
                ])

        return {
            "trip_id": trip_id,
            "added_stops": len(stops)
        }

    def get_stops(self):
        trip_id = self.context["trip_id"]
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT stop_order, stop_type, station_id, duration
                FROM bookings_tripstop
                WHERE trip_id = %s
                ORDER BY stop_order
            """, [trip_id])
            stops = cursor.fetchall()

        results = [
            {
                "stop_order": row[0],
                "stop_type": row[1],
                "station_id": row[2],
                "duration": str(row[3]) if row[3] is not None else None
            }
            for row in stops
        ]

        return results
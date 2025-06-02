from rest_framework import serializers
from django.db import connection


class RouteCreateSerializer(serializers.Serializer):
    origin_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
    origin_station_id = serializers.IntegerField(required=False, allow_null=True)
    destination_station_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        origin_id = data["origin_id"]
        destination_id = data["destination_id"]
        origin_station_id = data.get("origin_station_id")
        destination_station_id = data.get("destination_station_id")

        if origin_id == destination_id:
            raise serializers.ValidationError("Origin and destination locations must be different.")

        if origin_station_id and destination_station_id and origin_station_id == destination_station_id:
            raise serializers.ValidationError("Origin and destination stations must be different.")

        with connection.cursor() as cursor:
            if origin_station_id:
                cursor.execute("SELECT location_id FROM bookings_station WHERE station_id = %s", [origin_station_id])
                row = cursor.fetchone()
                if not row:
                    raise serializers.ValidationError("Origin station not found.")
                if row[0] != origin_id:
                    raise serializers.ValidationError("Origin station must belong to the origin location.")

            if destination_station_id:
                cursor.execute("SELECT location_id FROM bookings_station WHERE station_id = %s", [destination_station_id])
                row = cursor.fetchone()
                if not row:
                    raise serializers.ValidationError("Destination station not found.")
                if row[0] != destination_id:
                    raise serializers.ValidationError("Destination station must belong to the destination location.")

        return data

    def create(self, validated_data):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO bookings_route (origin_id, destination_id, origin_station_id, destination_station_id)
                VALUES (%s, %s, %s, %s)
                RETURNING route_id
            """, [
                validated_data["origin_id"],
                validated_data["destination_id"],
                validated_data.get("origin_station_id"),
                validated_data.get("destination_station_id")
            ])
            route_id = cursor.fetchone()[0]
        return {"route_id": route_id, **validated_data}


class RouteListSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    origin = serializers.CharField()
    destination = serializers.CharField()
    origin_station = serializers.CharField(allow_null=True)
    destination_station = serializers.CharField(allow_null=True)

    @classmethod
    def fetch_filtered(cls, filters):
        where = []
        params = []

        if filters.get("origin"):
            where.append("r.origin_id = %s")
            params.append(filters["origin"])

        if filters.get("destination"):
            where.append("r.destination_id = %s")
            params.append(filters["destination"])

        if filters.get("origin_station"):
            where.append("r.origin_station_iid = %s")
            params.append(filters["origin_station"])

        if filters.get("destination_station"):
            where.append("r.destination_station_id = %s")
            params.append(filters["destination_station"])

        where_clause = "WHERE " + " AND ".join(where) if where else ""

        query = f"""
            SELECT r.route_id,
                   l1.city || ', ' || l1.country AS origin,
                   l2.city || ', ' || l2.country AS destination,
                   s1.name AS origin_station,
                   s2.name AS destination_station
            FROM bookings_route r
            JOIN bookings_location l1 ON r.origin_id = l1.location_id
            JOIN bookings_location l2 ON r.destination_id = l2.location_id
            LEFT JOIN bookings_station s1 ON r.origin_station_id = s1.station_id
            LEFT JOIN bookings_station s2 ON r.destination_station_id = s2.station_id
            {where_clause}
            ORDER BY r.route_id
        """

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [
            cls({
                "route_id": r[0],
                "origin": r[1],
                "destination": r[2],
                "origin_station": r[3],
                "destination_station": r[4],
            }) for r in rows
        ]

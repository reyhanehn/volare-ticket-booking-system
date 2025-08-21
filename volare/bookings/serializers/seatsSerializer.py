from django.db import connection
from rest_framework import serializers

class AvailableSeatsSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(write_only=True)
    available_seats = serializers.ListField(
        child=serializers.IntegerField(), read_only=True
    )

    def to_representation(self, instance):
        ticket_id = instance["ticket_id"]

        sql = """
            SELECT s.seat
            FROM (
                SELECT generate_series(t.seat_start_number::int, t.seat_end_number::int) AS seat
                FROM bookings_ticket t
                WHERE t.ticket_id = %s
            ) s
            LEFT JOIN bookings_reservation r
              ON r.ticket_id = %s
             AND r.status NOT IN ('CANCELLED', 'EXPIRED')
             AND r.seat_number::int = s.seat
            WHERE r.seat_number IS NULL
            ORDER BY s.seat;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [ticket_id, ticket_id])
            rows = cursor.fetchall()
        available_seats = [row[0] for row in rows]

        return {"available_seats": available_seats}

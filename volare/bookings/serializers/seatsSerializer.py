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
             AND r.status NOT IN ('Cancelled')
             AND r.seat_number::int = s.seat
            WHERE r.seat_number IS NULL
            ORDER BY s.seat;
        """

        seat_start_num_sql = """
            SELECT seat_start_number
            FROM bookings_ticket t
            WHERE t.ticket_id = %s
        """

        seat_end_num_sql = """
            SELECT seat_end_number
            FROM bookings_ticket t
            WHERE t.ticket_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [ticket_id, ticket_id])
            rows = cursor.fetchall()
            cursor.execute(seat_start_num_sql, [ticket_id])
            start_num = cursor.fetchone()[0]
            cursor.execute(seat_end_num_sql, [ticket_id])
            end_num = cursor.fetchone()[0]
        available_seats = [row[0] for row in rows]

        return {
                    "available_seats": available_seats,
                    "total_seats": end_num - start_num + 1
                }

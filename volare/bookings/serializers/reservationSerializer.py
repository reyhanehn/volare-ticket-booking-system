from rest_framework import serializers
from django.db import connection
from django.utils import timezone
from datetime import timedelta

EXPIRATION_DURATION_MINUTES = 1
class ReservationSerializer(serializers.Serializer):
    passenger_id = serializers.IntegerField()
    ticket_id = serializers.IntegerField()
    seat_number = serializers.CharField(max_length=10)

    def validate(self, data):
        account_id = self.context['account_id']
        passenger_id = data['passenger_id']
        ticket_id = data['ticket_id']
        seat_number = data['seat_number']

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT related_account_id FROM bookings_passenger WHERE passenger_id = %s
            """, [passenger_id])
            result = cursor.fetchone()
            if not result or result[0] != account_id:
                raise serializers.ValidationError("Passenger does not belong to the logged-in account.")

            cursor.execute("""
                SELECT seat_start_number, seat_end_number FROM bookings_ticket WHERE ticket_id = %s
            """, [ticket_id])
            seat_info = cursor.fetchone()
            if not seat_info:
                raise serializers.ValidationError("Ticket not found.")
            try:
                seat_num_int = int(seat_number)
            except ValueError:
                raise serializers.ValidationError("Seat number must be numeric.")
            if not (seat_info[0] <= seat_num_int <= seat_info[1]):
                raise serializers.ValidationError("Seat number is out of range.")

            cursor.execute("""
                SELECT 1 FROM bookings_reservation WHERE ticket_id = %s AND seat_number = %s
            """, [ticket_id, seat_number])
            if cursor.fetchone():
                raise serializers.ValidationError("Seat already reserved.")

        return data

    def create(self, validated_data):
        expiration_duration = timedelta(minutes=EXPIRATION_DURATION_MINUTES)
        expiration_time = timezone.now() + expiration_duration
        account_id = self.context['account_id']

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO bookings_reservation
                (account_id, passenger_id, ticket_id, seat_number, status, reservation_date, reservation_time, expiration_time, cancelled_by_id)
                VALUES (%s, %s, %s, %s, 'Pending', CURRENT_DATE, CURRENT_TIME, %s, NULL)
                RETURNING reservation_id, reservation_date, reservation_time, expiration_time
            """, [
                account_id,
                validated_data['passenger_id'],
                validated_data['ticket_id'],
                validated_data['seat_number'],
                expiration_time,
            ])
            reservation_id, res_date, res_time, exp_time = cursor.fetchone()

        return {
            "reservation_id": reservation_id,
            **validated_data,
            "status": "Pending",
            "reservation_date": str(res_date),
            "reservation_time": str(res_time),
            "expiration_time": exp_time.isoformat()
        }

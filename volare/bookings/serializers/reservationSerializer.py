from rest_framework import serializers
from django.db import connection
from datetime import date, time
import re


class ReservationSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    passenger_id = serializers.IntegerField()
    ticket_id = serializers.IntegerField()
    seat_number = serializers.CharField(max_length=10)
    expiration = serializers.DurationField()

    def validate(self, data):
        account_id = data['account_id']
        passenger_id = data['passenger_id']
        ticket_id = data['ticket_id']
        seat_number = data['seat_number']

        with connection.cursor() as cursor:
            # 1. Validate passenger/account relationship
            cursor.execute("""
                           SELECT related_account_id
                           FROM bookings_passenger
                           WHERE passenger_id = %s
                           """, [passenger_id])
            result = cursor.fetchone()
            if not result:
                raise serializers.ValidationError("Passenger not found.")
            if result[0] != account_id:
                raise serializers.ValidationError("Passenger does not belong to the given account.")

            # 2. Validate seat number is within ticket's seat range
            cursor.execute("""
                           SELECT seat_start_number, seat_end_number
                           FROM bookings_ticket
                           WHERE ticket_id = %s
                           """, [ticket_id])
            seat_info = cursor.fetchone()
            if not seat_info:
                raise serializers.ValidationError("Ticket not found.")

            try:
                seat_num_int = int(seat_number)
            except ValueError:
                raise serializers.ValidationError("Seat number must be a numeric string.")

            start, end = seat_info
            if not (start <= seat_num_int <= end):
                raise serializers.ValidationError(f"Seat number must be between {start} and {end}.")

            # 3. Check if seat is already reserved
            cursor.execute("""
                           SELECT 1
                           FROM bookings_reservation
                           WHERE ticket_id = %s
                             AND seat_number = %s
                           """, [ticket_id, seat_number])
            if cursor.fetchone():
                raise serializers.ValidationError("This seat is already reserved.")

        return data

    def create(self, validated_data):
        with connection.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO bookings_reservation
                           (account_id, passenger_id, ticket_id, seat_number, status,
                            reservation_date, reservation_time, expiration, cancelled_by)
                           VALUES (%s, %s, %s, %s, 'Pending', CURRENT_DATE, CURRENT_TIME, %s,
                                   NULL) RETURNING reservation_id
                           """, [
                               validated_data['account_id'],
                               validated_data['passenger_id'],
                               validated_data['ticket_id'],
                               validated_data['seat_number'],
                               validated_data['expiration']
                           ])
            reservation_id = cursor.fetchone()[0]

        return {
            "reservation_id": reservation_id,
            **validated_data,
            "status": "Pending",
            "reservation_date": str(date.today()),
            "reservation_time": str(time.today().strftime('%H:%M:%S'))
        }

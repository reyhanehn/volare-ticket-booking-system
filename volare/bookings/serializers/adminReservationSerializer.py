from rest_framework import serializers
from django.db import connection
import re


class EditReservationSerializer(serializers.Serializer):
    seat_number = serializers.CharField(required=False)
    passenger_name = serializers.IntegerField(required=False)
    passenger_lastname = serializers.IntegerField(required=False)

    def validate_seat_number(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError("Seat number format is invalid.")
        return value

    def validate_passenger_name(self, value):
        if not re.match(r'^[a-zA-Z]+\s([a-zA-Z]+\s)*$', value):
            raise serializers.ValidationError("passenger name format is invalid.")
        return value

    def validate_passenger_lastname(self, value):
        if not re.match(r'^[a-zA-Z]+\s([a-zA-Z]+\s)*$', value):
            raise serializers.ValidationError("passenger last name format is invalid.")
        return value

    def validate(self, data):
        reservation_id = self.context["reservation_id"]
        new_seat = data.get("seat_number")
        new_name = data.get("passenger_name")
        new_lastname = data.get("passenger_lastname")

        if not (new_name or new_lastname or new_seat):
            raise serializers.ValidationError("You must at least change one thing")

        with connection.cursor() as cursor:
            cursor.execute("SELECT ticket_id, status, account_id FROM bookings_reservation WHERE reservation_id = %s", [reservation_id])
            row = cursor.fetchone()
            if not row:
                raise serializers.ValidationError("Reservation not found.")

            ticket_id, status, account_id = row

            if status == "Cancelled":
                raise serializers.ValidationError("Cannot edit a cancelled reservation.")

            if new_seat:
                cursor.execute("""
                    SELECT account_id FROM bookings_reservation
                    WHERE ticket_id = %s AND seat_number = %s AND reservation_id != %s
                """, [ticket_id, new_seat, reservation_id])
                if cursor.fetchone():
                    raise serializers.ValidationError("Seat number is already reserved.")

            if new_name or new_lastname:
                query = """
                    SELECT passenger_id
                    FROM bookings_passenger
                    WHERE related_account_id = %s
                """
                name_condition = "" if not new_name else f"AND name = {new_name} "
                lastname_condition = "" if not new_lastname else f"AND lastname = {new_lastname} "
                query = query + name_condition + lastname_condition
                cursor.execute(query, [account_id])
                passenger_id = cursor.fetchone()
                if not passenger_id:
                    raise serializers.ValidationError("passenger with this credentials does not exist")
                data["passenger_id"] = passenger_id

        return data

    def save(self):
        reservation_id = self.context["reservation_id"]
        new_seat = self.validated_data.get("seat_number")
        new_passenger = self.validated_data.get("passenger_id")

        with connection.cursor() as cursor:
            if new_seat:
                cursor.execute("""
                    UPDATE bookings_reservation
                    SET seat_number = %s
                    WHERE reservation_id = %s
                """, [new_seat, reservation_id])
            if new_passenger:
                cursor.execute("""
                    UPDATE bookings_reservation
                    SET passenger_id = %s
                    WHERE reservation_id = %s
                """, [new_passenger, reservation_id])

        return {"reservation_id": reservation_id, "new_seat": new_seat,
                "new_passenger": new_passenger, "message": "Reservation updated."}


class AdminConfirmReservationSerializer(serializers.Serializer):
    def validate(self, data):
        reservation_id = self.context["reservation_id"]

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.status, r.account_id, r.seat_number, r.ticket_id, 
                       p.name AS passenger_name, p.lastname AS passenger_lastname,
                       u.name AS user_name, u.lastname AS user_lastname, u.email
                FROM bookings_reservation r 
                JOIN bookings_passenger p ON r.passenger_id = p.passenger_id 
                JOIN account u ON u.account_id = r.account_id
                WHERE r.reservation_id = %s
            """, [reservation_id])
            reservation = cursor.fetchone()

            if not reservation:
                raise serializers.ValidationError("Reservation not found.")

            status, account_id, seat_number, ticket_id, passenger_name, passenger_lastname, user_name, user_lastname, email = reservation

            if status == "Confirmed":
                raise serializers.ValidationError("Reservation is already confirmed.")

            cursor.execute("""
                SELECT 
                vs.name AS section, v.type, o.city AS origin, d.city AS destination,
                trip.departure_datetime, t.price
                FROM bookings_ticket t
                JOIN bookings_trip trip ON t.trip_id = trip.trip_id
                JOIN companies_vehiclesection vs ON t.section_id = vs.section_id
                JOIN companies_vehicle v ON trip.vehicle_id = v.vehicle_id
                JOIN bookings_route r ON trip.route_id = r.route_id
                JOIN bookings_location o ON r.origin_id = o.location_id
                JOIN bookings_location d ON r.destination_id = d.location_id
                WHERE t.ticket_id = %s
            """, [ticket_id])
            ticket = cursor.fetchone()

            if not ticket:
                raise serializers.ValidationError("Ticket not found.")

        self.context.update({
            "reservation_id": reservation_id,
            "seat_number": seat_number,
            "ticket_id": ticket_id,
            "passenger_name": f"{passenger_name} {passenger_lastname}",
            "user_name": f"{user_name} {user_lastname}",
            "email": email,
            "section_name": ticket[0],
            "transport_type": ticket[1],
            "origin": ticket[2],
            "destination": ticket[3],
            "departure_datetime": str(ticket[4]),
            "amount": ticket[5],
            "currency": "IRR"
        })

        return data

    def save(self):
        reservation_id = self.context["reservation_id"]

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE bookings_reservation SET status = 'Confirmed' WHERE reservation_id = %s
            """, [reservation_id])

        return {
            "reservation_id": reservation_id,
            "name": self.context["user_name"],
            "email": self.context["email"],
            "passenger_name": self.context["passenger_name"],
            "origin": self.context["origin"],
            "destination": self.context["destination"],
            "departure_datetime": self.context["departure_datetime"],
            "seat_number": self.context["seat_number"],
            "section_name": self.context["section_name"],
            "transport_type": self.context["transport_type"],
            "amount": self.context["amount"],
            "currency": self.context["currency"]
        }


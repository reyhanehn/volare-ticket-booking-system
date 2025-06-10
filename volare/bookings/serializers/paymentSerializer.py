from rest_framework import serializers
from django.db import connection, transaction
from accounts.models.account import AccountRole


class ReservationPaymentSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=["Wallet", "Credit Card", "Cash", "PayPal", "Bank Transfer"])

    def validate(self, data):
        reservation_id = self.context["reservation_id"]
        user_id = self.context["user_id"]

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.status, r.account_id, t.price, t.ticket_id
                FROM bookings_reservation r
                JOIN bookings_ticket t ON r.ticket_id = t.ticket_id
                WHERE r.reservation_id = %s
            """, [reservation_id])
            row = cursor.fetchone()

            if not row:
                raise serializers.ValidationError("Reservation not found.")

            status_, account_id, price, ticket_id = row

            if account_id != user_id:
                raise serializers.ValidationError("You do not have permission to pay for this reservation.")

            if status_ == "Confirmed":
                raise serializers.ValidationError("Reservation is already paid and confirmed.")

            data["price"] = price
            data["account_id"] = account_id
            data["ticket_id"] = ticket_id

            if data["method"] == "Wallet":
                cursor.execute("""
                    SELECT wallet_id, balance FROM wallet WHERE account_id = %s
                """, [account_id])
                wallet = cursor.fetchone()
                if not wallet:
                    raise serializers.ValidationError("Wallet not found.")

                wallet_id, balance = wallet
                if balance < price:
                    raise serializers.ValidationError("Insufficient wallet balance.")

                data["wallet_id"] = wallet_id

        return data

    def save(self):
        reservation_id = self.context["reservation_id"]
        method = self.validated_data["method"]
        price = self.validated_data["price"]
        account_id = self.validated_data["account_id"]

        with transaction.atomic():
            with connection.cursor() as cursor:
                if method == "Wallet":
                    wallet_id = self.validated_data["wallet_id"]

                    # Deduct balance
                    cursor.execute("""
                        UPDATE wallet SET balance = balance - %s WHERE wallet_id = %s
                    """, [price, wallet_id])

                    # Log wallet transaction
                    cursor.execute("""
                        INSERT INTO wallet_transactions (wallet_id, amount, type, transaction_date, transaction_time)
                        VALUES (%s, %s, 'Payment', CURRENT_DATE, CURRENT_TIME)
                    """, [wallet_id, price])

                # Create payment record
                cursor.execute("""
                    INSERT INTO bookings_payment (account_id, reservation_id, amount, payment_method, status, payment_date, payment_time)
                    VALUES (%s, %s, %s, %s, 'Completed', CURRENT_DATE, CURRENT_TIME)
                """, [account_id, reservation_id, price, method])

                # Update reservation status
                cursor.execute("""
                    UPDATE bookings_reservation SET status = 'Confirmed' WHERE reservation_id = %s
                """, [reservation_id])

        return {
            "message": "Payment successful.",
            "reservation_id": reservation_id,
            "amount": price,
            "method": method
        }


class PaymentStatusSerializer(serializers.Serializer):
    def validate(self, data):
        reservation_id = self.context["reservation_id"]
        user_id = self.context["user_id"]

        with connection.cursor() as cursor:
            cursor.execute("""
                            SELECT account_id, role FROM account WHERE account_id = %s
                        """, [user_id])
            row = cursor.fetchone()
            if not row:
                raise serializers.ValidationError("User doesn't exist")
            role = row[1]
            if role == AccountRole.CUSTOMER.value:
                cursor.execute("""
                    SELECT r.account_id FROM bookings_reservation r WHERE r.reservation_id = %s
                """, [reservation_id])
                res = cursor.fetchone()
                if not res:
                    raise serializers.ValidationError("Reservation not found.")

                if res[0] != user_id:
                    raise serializers.ValidationError("You do not have permission to view this reservation.")

            self.context["role"] = role

        return data

    def get_status(self):
        reservation_id = self.context["reservation_id"]
        role = self.context["role"]

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.status, r.seat_number, r.reservation_date, r.ticket_id,  
                       p.name AS passenger_name, p.lastname AS passenger_lastname,
                       u.name AS user_name, u.lastname AS user_lastname
                FROM bookings_reservation r 
                JOIN bookings_passenger p ON r.passenger_id = p.passenger_id 
                JOIN account u ON u.account_id = r.account_id
                WHERE reservation_id = %s
            """, [reservation_id])
            reservation = cursor.fetchone()

            if not reservation:
                raise serializers.ValidationError("Reservation does not exist")

            cursor.execute("""
                SELECT status, payment_method, amount, payment_date, payment_time
                FROM bookings_payment
                WHERE reservation_id = %s
            """, [reservation_id])
            payment = cursor.fetchone()

            cursor.execute("""
                SELECT wt.amount, wt.transaction_date, wt.transaction_time
                FROM wallet_transactions wt
                JOIN bookings_payment p ON wt.related_payment_id_id = p.payment_id
                WHERE p.reservation_id = %s
            """, [reservation_id])
            refund = cursor.fetchone()

        # Unpack reservation fields
        status, seat_number, _, ticket_id, passenger_name, passenger_lastname, user_name, user_lastname = reservation
        passenger_full_name = f"{passenger_name} {passenger_lastname}"
        user_full_name = f"{user_name} {user_lastname}"

        reservation_info = {
            "id": reservation_id,
            "ticket": ticket_id,
            "status": status,
            "seat": seat_number,
            "passenger": passenger_full_name
        }

        if not payment:
            if role == AccountRole.CUSTOMER.value:
                return reservation_info
            else:
                return {
                    "user info": user_full_name,
                    **reservation_info
                }

        payment_info = {
            "status": payment[0],
            "method": payment[1],
            "amount": payment[2],
            "paid_on": payment[3],
            "paid_at": str(payment[4]),
            "reservation": reservation_info
        }

        if role != AccountRole.CUSTOMER.value:
            payment_info["user info"] = user_full_name

        if refund:
            refund_info = {
                "amount": refund[0],
                "date": refund[1],
                "time": refund[2]
            }
            payment_info["refund info"] = refund_info

        return payment_info


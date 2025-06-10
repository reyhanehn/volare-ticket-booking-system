from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from datetime import datetime
from accounts.permissions import IsAdmin


class AdminCancelReservationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        reservation_id = request.data.get("reservation_id")
        if not reservation_id:
            return Response({"error": "reservation_id is required"}, status=400)

        admin = request.user

        with connection.cursor() as cursor:
            # Step 1: Fetch reservation and user info
            cursor.execute("""
                SELECT r.reservation_id, r.account_id, r.status, t.price, a.name, a.email
                FROM bookings_reservation r
                JOIN account a ON r.account_id = a.account_id
                JOIN bookings_ticket t ON r.ticket_id = t.ticket_id
                WHERE r.reservation_id = %s
            """, [reservation_id])
            row = cursor.fetchone()

            if not row:
                return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

            res_id, user_id, status_val, price, user_name, user_email = row
            status_val = status_val.lower()

            if status_val == "cancelled":
                return Response({"error": "Reservation already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

            refund_amount = 0  # default

            if status_val == "confirmed":
                # Step 2: Must find a payment for confirmed reservation
                cursor.execute("SELECT payment_id FROM bookings_payment WHERE reservation_id = %s", [reservation_id])
                payment_row = cursor.fetchone()

                if not payment_row:
                    return Response({"error": "No payment found for a confirmed reservation!"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                payment_id = payment_row[0]

                # Step 3: Refund to wallet
                cursor.execute("SELECT wallet_id, balance FROM wallet WHERE account_id = %s", [user_id])
                wallet = cursor.fetchone()

                if wallet:
                    wallet_id, balance = wallet
                    cursor.execute("UPDATE wallet SET balance = balance + %s WHERE wallet_id = %s", [price, wallet_id])
                else:
                    cursor.execute("INSERT INTO wallet (account_id, balance) VALUES (%s, %s) RETURNING wallet_id",
                                   [user_id, price])
                    wallet_id = cursor.fetchone()[0]

                # Step 4: Log wallet transaction
                now = datetime.now()
                cursor.execute("""
                    INSERT INTO wallet_transactions 
                    (wallet_id, amount, type, transaction_date, transaction_time, related_payment_id_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [wallet_id, price, 'Refund', now.date(), now.time(), payment_id])

                refund_amount = price

            # Step 5: Mark reservation as cancelled
            cursor.execute("""
                UPDATE bookings_reservation
                SET status = %s, cancelled_by_id = %s
                WHERE reservation_id = %s
            """, ['Cancelled', admin.account_id, reservation_id])

        # Step 6: Send email
        html_message = render_to_string('emails/admin_cancel_notice.html', {
            'name': user_name,
            'reservation_id': reservation_id,
            'admin_name': admin.name,
            'refund_amount': refund_amount,
            'was_refunded': status_val == "confirmed",
        })

        send_mail(
            subject="Reservation Cancelled by Administrator",
            message="Your reservation has been cancelled.",
            from_email="astheshriketoyoursharp@gmail.com",
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False
        )

        return Response({
            "message": "Reservation cancelled, user notified.",
            "reservation_id": reservation_id,
            "refund_amount": refund_amount
        }, status=status.HTTP_200_OK)

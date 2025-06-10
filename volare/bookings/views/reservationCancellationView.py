from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

class ReservationCancelInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reservation_id = request.data.get('reservation_id')
        account_id = request.user.account_id

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.reservation_id, r.seat_number, r.status, r.reservation_date,
                       r.reservation_time, r.expiration_time, r.ticket_id, r.passenger_id,
                       t.price
                FROM bookings_reservation r
                JOIN bookings_ticket t ON r.ticket_id = t.ticket_id
                WHERE r.reservation_id = %s AND r.account_id = %s
            """, [reservation_id, account_id])
            result = cursor.fetchone()

        if not result:
            return Response({"error": "Reservation not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

        (
            res_id, seat_number, res_status, res_date, res_time,
            expiration_time, ticket_id, passenger_id, ticket_price
        ) = result

        reservation_info = {
            "reservation_id": res_id,
            "seat_number": seat_number,
            "status": res_status,
            "reservation_date": str(res_date),
            "reservation_time": str(res_time),
            "ticket_id": ticket_id,
            "passenger_id": passenger_id,
            "expiration_time": expiration_time.isoformat(),
        }

        if res_status == "Pending":
            return Response({
                "reservation": reservation_info,
                "ticket_price": float(ticket_price)
            }, status=status.HTTP_200_OK)

        penalty_percentage = 10
        penalty_amount = round(ticket_price * penalty_percentage / 100, 2)
        refund_amount = round(ticket_price - penalty_amount, 2)

        return Response({
            "reservation": reservation_info,
            "ticket_price": float(ticket_price),
            "penalty_percentage": penalty_percentage,
            "penalty_amount": penalty_amount,
            "refund_amount": refund_amount
        }, status=status.HTTP_200_OK)


class ReservationCancelConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        reservation_id = request.data.get("reservation_id")
        new_status = request.data.get("status")
        account_id = request.user.account_id

        if new_status != "Cancelled":
            return Response({"error": "Only status='Cancelled' is allowed."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.ticket_id, t.price, r.status
                FROM bookings_reservation r
                JOIN bookings_ticket t ON r.ticket_id = t.ticket_id
                WHERE r.reservation_id = %s AND r.account_id = %s
            """, [reservation_id, account_id])
            result = cursor.fetchone()

            if not result:
                return Response({"error": "Reservation not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

            ticket_id, ticket_price, current_status = result

            if current_status == "Cancelled":
                return Response({"error": "Reservation is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

            cursor.execute("""
                UPDATE bookings_reservation
                SET status = 'Cancelled',
                    expiration_time = NOW(),
                    cancelled_by_id = NULL
                WHERE reservation_id = %s AND account_id = %s
            """, [reservation_id, account_id])

            if current_status == "Pending":
                return Response({
                    "message": "Pending reservation cancelled. No refund issued."
                }, status=status.HTTP_200_OK)

            cursor.execute("SELECT wallet_id FROM wallet WHERE account_id = %s", [account_id])
            wallet_row = cursor.fetchone()
            if not wallet_row:
                return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

            wallet_id = wallet_row[0]

            cursor.execute("""
                SELECT payment_id, amount, status FROM bookings_payment
                WHERE reservation_id = %s AND account_id = %s
            """, [reservation_id, account_id])
            payment = cursor.fetchone()

            if not payment:
                return Response({"error": "Payment not found for confirmed reservation."}, status=status.HTTP_400_BAD_REQUEST)

            payment_id, amount_paid, payment_status = payment

            if payment_status != "Completed":
                return Response({"error": "Only completed payments can be refunded."}, status=status.HTTP_400_BAD_REQUEST)

            penalty_percentage = 10
            penalty_amount = round(amount_paid * penalty_percentage / 100, 2)
            refund_amount = round(amount_paid - penalty_amount, 2)

            cursor.execute("""
                UPDATE wallet SET balance = balance + %s WHERE wallet_id = %s
            """, [refund_amount, wallet_id])

            cursor.execute("""
                INSERT INTO wallet_transactions
                (wallet_id, amount, type, transaction_date, transaction_time, related_payment_id_id)
                VALUES (%s, %s, 'Refund', CURRENT_DATE, CURRENT_TIME, %s)
            """, [wallet_id, refund_amount, payment_id])

            cursor.execute("""
                UPDATE bookings_payment SET status = 'Refunded' WHERE payment_id = %s
            """, [payment_id])

        return Response({
            "message": "Reservation cancelled and refund issued to wallet.",
            "refund_amount": refund_amount
        }, status=status.HTTP_200_OK)

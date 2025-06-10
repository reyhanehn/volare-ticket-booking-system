from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin
from django.db import connection
from ..serializers.reservationEditSerializer import EditReservationSerializer


class AdminEditReservationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, reservation_id):
        serializer = EditReservationSerializer(data=request.data, context={"reservation_id": reservation_id})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminConfirmReservationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, reservation_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT status FROM bookings_reservation WHERE reservation_id = %s
            """, [reservation_id])
            row = cursor.fetchone()
            if not row:
                return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

            current_status = row[0]
            if current_status == "Confirmed":
                return Response({"message": "Reservation is already confirmed."}, status=status.HTTP_200_OK)

            if current_status == "Cancelled":
                return Response({"error": "Cannot confirm a cancelled reservation."}, status=status.HTTP_400_BAD_REQUEST)

            cursor.execute("""
                UPDATE bookings_reservation SET status = 'Confirmed' WHERE reservation_id = %s
            """, [reservation_id])

        return Response({"message": "Reservation confirmed successfully.", "reservation_id": reservation_id}, status=status.HTTP_200_OK)
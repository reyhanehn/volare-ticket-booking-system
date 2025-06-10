from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.utils.dateparse import parse_date
from ..serializers.reservationSerializer import ReservationSerializer
from accounts.permissions import IsAdmin


class CreateReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data, context={'account_id': request.user.account_id})
        if serializer.is_valid():
            # The serializer.save() already uses raw SQL as you showed before,
            # so just call it directly here
            reservation = serializer.save()
            return Response({
                "message": "Reservation created successfully",
                "data": reservation
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account_id = request.user.account_id
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    r.reservation_id, r.seat_number, r.status, r.reservation_date, r.reservation_time,
                    p.passenger_id, t.ticket_id
                FROM bookings_reservation r
                JOIN bookings_passenger p ON r.passenger_id = p.passenger_id
                JOIN bookings_ticket t ON r.ticket_id = t.ticket_id
                WHERE r.account_id = %s
            """, [account_id])
            rows = cursor.fetchall()

        data = []
        for row in rows:
            reservation_id, seat_number, status_, reservation_date, reservation_time, passenger_id, ticket_id = row
            data.append({
                "reservation_id": reservation_id,
                "seat_number": seat_number,
                "status": status_,
                "reservation_date": str(reservation_date),
                "reservation_time": str(reservation_time),
                "passenger_id": passenger_id,
                "ticket_id": ticket_id,
            })

        return Response({"reservations": data}, status=status.HTTP_200_OK)


class AdminReservationFilterView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        status_param = request.GET.get('status')
        date_param = request.GET.get('date')

        sql = """
            SELECT 
                r.reservation_id, r.seat_number, r.status, r.reservation_date, r.reservation_time,
                p.passenger_id, t.ticket_id, a.account_id
            FROM bookings_reservation r
            JOIN bookings_passenger p ON r.passenger_id = p.passenger_id
            JOIN bookings_ticket t ON r.ticket_id = t.ticket_id
            JOIN account a ON r.account_id = a.account_id
            WHERE 1=1
        """
        params = []
        if status_param:
            sql += " AND r.status = %s"
            params.append(status_param)
        if date_param:
            parsed_date = parse_date(date_param)
            if parsed_date:
                sql += " AND r.reservation_date = %s"
                params.append(parsed_date)

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        data = []
        for row in rows:
            reservation_id, seat_number, status_, reservation_date, reservation_time, passenger_id, ticket_id, account_id = row
            data.append({
                "reservation_id": reservation_id,
                "seat_number": seat_number,
                "status": status_,
                "reservation_date": str(reservation_date),
                "reservation_time": str(reservation_time),
                "passenger_id": passenger_id,
                "ticket_id": ticket_id,
                "account_id": account_id
            })

        return Response({"reservations": data}, status=status.HTTP_200_OK)

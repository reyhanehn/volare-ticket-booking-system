from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import Reservation
from ..serializers.reservationSerializer import ReservationSerializer

class CreateReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            return Response({
                "message": "Reservation created successfully",
                "data": reservation
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            return Response({
                "message": "Reservation created successfully",
                "data": reservation
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        account = request.user  # assumes request.user is the Account instance
        reservations = Reservation.objects.filter(account=account).select_related("ticket", "passenger")

        data = []
        for res in reservations:
            data.append({
                "reservation_id": res.reservation_id,
                "seat_number": res.seat_number,
                "status": res.status,
                "reservation_date": str(res.reservation_date),
                "reservation_time": str(res.reservation_time),
                "expiration": str(res.expiration),
                "passenger_id": res.passenger.passenger_id,
                "ticket_id": res.ticket.ticket_id,
            })

        return Response({"reservations": data}, status=status.HTTP_200_OK)
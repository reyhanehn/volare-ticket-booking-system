from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from ..models import Reservation, ReservationStatus
from ..serializers.reservationSerializer import ReservationSerializer

# User: Create Reservation
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

# User: View Own Reservations
class ReservationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user
        reservations = Reservation.objects.filter(account=account).select_related("ticket", "passenger")

        data = []
        for res in reservations:
            data.append({
                "reservation_id": res.reservation_id,
                "seat_number": res.seat_number,
                "status": res.status,
                "reservation_date": str(res.reservation_date),
                "reservation_time": str(res.reservation_time),
                "passenger_id": res.passenger.passenger_id,
                "ticket_id": res.ticket.ticket_id,
            })

        return Response({"reservations": data}, status=status.HTTP_200_OK)

# Admin: Filter All Reservations
class AdminReservationFilterView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        status_param = request.GET.get('status')
        date_param = request.GET.get('date')
        query = Reservation.objects.select_related('passenger', 'ticket', 'account')

        if status_param:
            query = query.filter(status=status_param)
        if date_param:
            query = query.filter(reservation_date=parse_date(date_param))

        reservations = query.all()
        data = []
        for res in reservations:
            data.append({
                "reservation_id": res.reservation_id,
                "seat_number": res.seat_number,
                "status": res.status,
                "reservation_date": str(res.reservation_date),
                "reservation_time": str(res.reservation_time),
                "passenger_id": res.passenger.passenger_id,
                "ticket_id": res.ticket.ticket_id,
                "account_id": res.account.id
            })
        return Response({"reservations": data}, status=status.HTTP_200_OK)

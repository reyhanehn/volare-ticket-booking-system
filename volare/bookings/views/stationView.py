from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

from bookings.serializers.stationSerializer import StationSerializer
from accounts.permissions import IsAnyAdmin

class CreateStationView(APIView):
    permission_classes = [IsAuthenticated, IsAnyAdmin]

    def post(self, request):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            station = serializer.save()
            return Response(station, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT station_id, name, type, location_id FROM bookings_station ORDER BY station_id ASC")
            rows = cursor.fetchall()
        stations = [
            {"station_id": sid, "name": name, "type": stype, "location": loc}
            for sid, name, stype, loc in rows
        ]
        return Response({'stations': stations}, status=status.HTTP_200_OK)

# stations/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from .models import Station
from bookings.serializers.stationSerializer import StationSerializer
from accounts.permissions import IsAdmin

from ..models.location import Station


class CreateStationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            station = serializer.save()
            return Response(StationSerializer(station).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class StationListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        return Response({'stations': serializer.data}, status=status.HTTP_200_OK)
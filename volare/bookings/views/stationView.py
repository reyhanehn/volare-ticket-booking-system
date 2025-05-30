# stations/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Station
from .serializers import StationSerializer

class StationView(APIView):
    def get(self, request):
        stations = Station.objects.select_related('location').all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            station = serializer.save()
            return Response(StationSerializer(station).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

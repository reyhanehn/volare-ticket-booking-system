from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import connection

from ..serializers.locationSerializer import LocationSerializer
from accounts.permissions import IsAdmin


class CreateLocationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.save()
            return Response({
                'message': 'Location created successfully',
                'data': location
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        with connection.cursor() as cursor:
            # CORRECTED: Change 'id' to 'location_id' in the SELECT statement
            cursor.execute("SELECT location_id, country, city FROM bookings_location ORDER BY country, city")
            rows = cursor.fetchall()

        # CORRECTED: Change the variable and dictionary key to match
        locations = [{'id': location_id, 'country': country, 'city': city} for location_id, country, city in rows]

        return Response({'locations': locations}, status=status.HTTP_200_OK)

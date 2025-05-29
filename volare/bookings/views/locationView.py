# volare/bookings/views/location_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from volare.bookings.serializers.locationSerializer import LocationSerializer
from volare.accounts.permissions import IsAdmin

class CreateLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Location created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

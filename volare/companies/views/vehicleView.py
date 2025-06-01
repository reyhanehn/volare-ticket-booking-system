# vehicles/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..serializers.vehicleSerializer import VehicleSerializer
from accounts.permissions import IsCompanyOwner


class CreateVehicleView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwner]

    def post(self, request):
        serializer = VehicleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Automatically get the company of the logged-in company owner
            company = request.user.company
            vehicle = serializer.save(company=company)

            return Response({
                'message': 'Vehicle created successfully',
                'vehicle_id': vehicle.vehicle_id,
                'data': VehicleSerializer(vehicle).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': 'Invalid data provided',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

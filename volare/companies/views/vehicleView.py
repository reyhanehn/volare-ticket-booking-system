from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.vehicleSerializer import VehicleSerializer
from accounts.permissions import IsCompanyAdmin



class CreateVehicleView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def post(self, request):
        serializer = VehicleSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            vehicle = serializer.save()  # serializer uses raw SQL internally
            return Response({
                'message': 'Vehicle and sections created successfully',
                'vehicle_id': vehicle.vehicle_id,
                'data': VehicleSerializer(vehicle).data  # re-serialize for response
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

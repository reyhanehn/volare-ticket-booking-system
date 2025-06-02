from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAnyAdmin
from ..serializers.vehicleServiceSerializer import VehicleServiceAssignSerializer


class AssignServicesToVehicleView(APIView):
    permission_classes = [IsAuthenticated, IsAnyAdmin]

    def post(self, request):
        serializer = VehicleServiceAssignSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({
                "message": "Services assigned successfully.",
                "vehicle_id": result["vehicle_id"],
                "assigned_service_ids": result["assigned_services"]
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

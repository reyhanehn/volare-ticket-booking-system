from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.tripStopSerializer import TripStopCreateSerializer
from accounts.permissions import IsCompanyAdmin


class TripStopView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def post(self, request, trip_id):
        serializer = TripStopCreateSerializer(data=request.data, context={"trip_id": trip_id})
        if serializer.is_valid():
            result = serializer.save()
            return Response({
                "message": "Trip stops added successfully.",
                "details": result
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, trip_id):
        serializer = TripStopCreateSerializer(data=request.data, context={"trip_id": trip_id})
        results = serializer.get_stops()
        return Response({
            "trip_id": trip_id,
            "stops": results
        }, status=status.HTTP_200_OK)

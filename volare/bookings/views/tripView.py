from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCompanyAdmin
from ..serializers.tripSerializer import TripCreateSerializer


class TripCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def post(self, request):
        serializer = TripCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            trip = serializer.save()
            return Response({
                "message": "Trip and tickets created successfully",
                "trip": trip
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.seatsSerializer import AvailableSeatsSerializer

class AvailableSeatsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, ticket_id: int):
        serializer = AvailableSeatsSerializer({"ticket_id": ticket_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

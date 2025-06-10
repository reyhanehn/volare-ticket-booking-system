from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers.ticketSerializer import TicketSearchSerializer, TicketDetailSerializer


class TicketCacheDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, ticket_id):
        serializer = TicketDetailSerializer(data={"ticket_id": ticket_id})
        serializer.is_valid(raise_exception=True)

        ticket_data = serializer.data
        if not ticket_data:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(ticket_data, status=status.HTTP_200_OK)


class TicketSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = TicketSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            results = serializer.search()
            return Response(results)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
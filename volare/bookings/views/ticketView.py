from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers.ticketSerializer import TicketSearchSerializer, TicketDetailSerializer, AdminTicketListSerializer, CompanyTicketListSerializer
from accounts.permissions import IsAdmin, IsCompanyAdmin
from django.db import connection
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView
from ..models import Trip
from ..serializers.ticketSerializer import TripUpdateSerializer


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

class AdminTicketListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        serializer = AdminTicketListSerializer(data=request.query_params)
        if serializer.is_valid():
            result = serializer.search()
            return Response(result)
        return Response(serializer.errors, status=400)


class CompanyTicketListView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT company_id FROM companies_company WHERE owner_id = %s
            """,[request.user.account_id])
            company_id = cursor.fetchone()

        if not company_id:
            raise serializers.ValidationError("Company does not exist")

        serializer = CompanyTicketListSerializer(
            data=request.query_params,
            context={"company_id": company_id}
        )
        if serializer.is_valid():
            result = serializer.search()
            return Response(result)
        return Response(serializer.errors, status=400)


class TripUpdateRawView(UpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripUpdateSerializer
    permission_classes = [IsAdmin]

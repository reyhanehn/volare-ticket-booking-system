
from ..serializers.vehicleSerializer import VehicleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsCompanyAdmin
from django.db import connection
from rest_framework import status




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




class GetAllVehiclesView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    v.vehicle_id,
                    v.name,
                    v.type,
                    v.class_code,
                    v.total_seats,
                    v.layout,
                    v.company_id,
                    c.name AS company_name
                FROM companies_vehicle v
                JOIN companies_company c ON v.company_id = c.company_id
            """)
            rows = cursor.fetchall()

            vehicles = [
                {
                    "vehicle_id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "class_code": row[3],
                    "total_seats": row[4],
                    "layout": row[5],
                    "company_id": row[6],
                    "company_name": row[7],
                }
                for row in rows
            ]

        return Response({
            "count": len(vehicles),
            "vehicles": vehicles
        }, status=status.HTTP_200_OK)

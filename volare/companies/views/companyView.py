from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsAdmin, IsCompanyAdmin
from ..serializers.companySerializer import CompanyCreateSerializer
from django.db import connection

class CreateCompanyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CompanyCreateSerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()
            return Response({
                'message': 'Company and company owner created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCompaniesView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    c.company_id, 
                    c.name, 
                    c.logo_url, 
                    c.website, 
                    a.account_id AS owner_id, 
                    a.email AS owner_email
                FROM companies_company c
                JOIN account a ON c.owner_id = a.account_id
            """)
            rows = cursor.fetchall()

            companies = [
                {
                    "company_id": row[0],
                    "name": row[1],
                    "logo_url": row[2],
                    "website": row[3],
                    "owner_id": row[4],
                    "owner_email": row[5]
                }
                for row in rows
            ]

        return Response({
            "count": len(companies),
            "companies": companies
        }, status=status.HTTP_200_OK)

# companies/views/companyViews.py


class GetMyCompanyView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get(self, request):
        owner_id = request.user.account_id

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT company_id, name, logo_url, website, owner_id
                FROM companies_company
                WHERE owner_id = %s
            """, [owner_id])
            result = cursor.fetchone()

        if not result:
            return Response(
                {"detail": "Company not found for this owner."},
                status=status.HTTP_404_NOT_FOUND
            )

        company_data = {
            "company_id": result[0],
            "name": result[1],
            "logo_url": result[2],
            "website": result[3],
            "owner_id": result[4]
        }

        return Response(company_data, status=status.HTTP_200_OK)

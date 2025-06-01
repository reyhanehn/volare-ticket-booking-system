from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsAdmin
from ..serializers.companySerializer import CompanyCreateSerializer

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

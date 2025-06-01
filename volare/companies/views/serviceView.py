from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAnyAdmin
from ..serializers.serviceSerializer import ServiceCreateSerializer, ServiceListSerializer


class CreateServiceView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = ServiceCreateSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            return Response({
                "message": "Service created successfully",
                "service": {
                    "id": service.service_id,
                    "name": service.name
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceListView(APIView):
    permission_classes = [IsAuthenticated, IsAnyAdmin]

    def get(self, request):
        services = ServiceListSerializer.fetch_all()
        data = [s.data for s in services]
        return Response(data)

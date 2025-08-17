from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAnyAdmin
from ..serializers.routeSerializer import RouteCreateSerializer, RouteListSerializer


class RouteCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAnyAdmin]

    def post(self, request):
        serializer = RouteCreateSerializer(data=request.data)
        if serializer.is_valid():
            route = serializer.save()
            return Response({
                "message": "Route created successfully",
                "route": route
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {
            "origin": request.query_params.get("origin"),
            "destination": request.query_params.get("destination"),
            "origin_station": request.query_params.get("origin_station"),
            "destination_station": request.query_params.get("destination_station"),
        }
        filters = {k: int(v) for k, v in filters.items() if v is not None}

        routes = RouteListSerializer.fetch_filtered(filters)
        return Response([r.data for r in routes])
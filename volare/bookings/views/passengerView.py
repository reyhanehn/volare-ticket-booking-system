from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers.passengerSerializer import CreatePassengerSerializer, PassengerListSerializer


class CreatePassengerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePassengerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            passenger = serializer.save()
            return Response(passenger, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassengerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = PassengerListSerializer.get_passengers(request.user.account_id)
        return Response(data)

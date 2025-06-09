from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.paymentSerializer import ReservationPaymentSerializer, PaymentStatusSerializer


class ReservationPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        serializer = ReservationPaymentSerializer(
            data=request.data,
            context={
                "reservation_id": reservation_id,
                "user_id": request.user.account_id
            }
        )
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id):
        serializer = PaymentStatusSerializer(data={}, context={
            "reservation_id": reservation_id,
            "user_id": request.user.account_id
        })
        if serializer.is_valid():
            result = serializer.get_status()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
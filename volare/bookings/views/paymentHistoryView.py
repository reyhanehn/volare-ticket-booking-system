from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.paymentHistorySerializer import PaymentHistorySerializer

class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PaymentHistorySerializer(data=request.query_params, context={"user_id": request.user.account_id})
        if serializer.is_valid():
            result = serializer.get_history()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..serializers.wallet_transactionsSerializer import WalletChargeSerializer


class WalletChargeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WalletChargeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            transaction = serializer.save()

            return Response({
                'message': 'Wallet charged successfully.',
                'transaction': {
                    'transaction_id': transaction.transaction_id,
                    'wallet_id': transaction.wallet_id,
                    'amount': float(transaction.amount),
                    'type': transaction.type,
                    'transaction_date': transaction.transaction_date,
                    'transaction_time': transaction.transaction_time,
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

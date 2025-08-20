from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers.walletSerializer import WalletSerializer

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = WalletSerializer.from_account(request.user.account_id)
        return Response(serializer.data)

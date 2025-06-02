from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from ..serializers.passwordLoginSerializer import PasswordLoginSerializer


class PasswordLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            password = serializer.validated_data["password"]

            if not check_password(password, user.password_hash):
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
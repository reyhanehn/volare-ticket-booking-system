# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSignupSerializer
from .Models import Account
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
    def post(self, request):
        serializer = AccountSignupSerializer(data=request.data)
        if serializer.is_valid():
            # Save the account (handles password hashing in serializer)
            account = serializer.save()

            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(account)

            return Response({
                'message': 'Account created successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import json

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.signupSerializer import AccountSignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from redis_client import redis_client


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountSignupSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()

            self.cache_user_data(account)

            refresh = RefreshToken.for_user(account)

            return Response({
                'message': 'Account created successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def cache_user_data(user):
        key = user.account_id
        user_data = {
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "status": user.status,
            "registration_date": str(user.registration_date),
            "birthdate": str(user.birth_date),
            "city": user.city_id
        }
        redis_client.setex(key, 3600 * 6, json.dumps(user_data))  # expires in 6 hours

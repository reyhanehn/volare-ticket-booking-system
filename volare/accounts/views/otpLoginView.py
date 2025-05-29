import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.otpLoginSerializer import RequestOTPSerializer
from ..serializers.otpLoginSerializer import VerifyOTPSerializer
from ..redis_client import redis_client


class RequestOTPView(APIView):
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']

            otp = f"{random.randint(100000, 999999)}"

            # Store OTP in Redis with key pattern "otp:<user_id>", expires in 5 minutes (300 seconds)
            redis_client.setex(f"otp:{user.id}", 300, otp)
            # Send OTP via SMS/email here

            return Response({"message": f"OTP sent {otp}"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            input_otp = serializer.validated_data["otp"]

            expected_otp = redis_client.get(f"otp:{user.id}")
            if expected_otp is None:
                return Response({'error': 'OTP expired or not found'}, status=status.HTTP_400_BAD_REQUEST)

            if input_otp != expected_otp.decode():
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            # OTP is valid
            redis_client.delete(f"otp:{user.id}")  # remove it after use

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

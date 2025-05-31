import random

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.otpLoginSerializer import RequestOTPSerializer
from ..serializers.otpLoginSerializer import VerifyOTPSerializer
from ..redis_client import redis_client
from django.core.mail import send_mail


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']
            otp = f"{random.randint(100000, 999999)}"

            redis_client.setex(f"otp:{user.account_id}", 300, otp)

            if user.email:
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP code is: {otp}",
                    from_email="astheshriketoyoursharp@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)

            return Response({"error": "User does not have an email address"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            input_otp = serializer.validated_data["otp"]

            expected_otp = redis_client.get(f"otp:{user.account_id}")
            if expected_otp is None:
                return Response({'error': 'OTP expired or not found'}, status=status.HTTP_400_BAD_REQUEST)

            if input_otp != expected_otp.decode():
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            redis_client.delete(f"otp:{user.account_id}")

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

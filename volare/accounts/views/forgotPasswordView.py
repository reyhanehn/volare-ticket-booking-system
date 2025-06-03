import random

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from redis_client import redis_client
from ..serializers.forgotPasswordSerializer import (
    RequestForgotPasswordSerializer,
    VerifyForgotPasswordSerializer
)


class RequestForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context["user"]
            otp = f"{random.randint(100000, 999999)}"
            redis_client.setex(f"reset_otp:{user.account_id}", 300, otp)  # 5 mins

            if user.email:
                send_mail(
                    subject="Reset Your Password",
                    message=f"Your OTP to reset password is: {otp}",
                    from_email="astheshriketoyoursharp@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)

            return Response({"error": "User has no email configured"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            input_otp = serializer.validated_data["otp"]
            new_password = serializer.validated_data["new_password"]

            expected_otp = redis_client.get(f"reset_otp:{user.account_id}")
            if expected_otp is None:
                return Response({'error': 'OTP expired or not found'}, status=status.HTTP_400_BAD_REQUEST)

            if input_otp != expected_otp.decode():
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            user.password_hash = make_password(new_password)
            user.save()
            redis_client.delete(f"reset_otp:{user.account_id}")

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

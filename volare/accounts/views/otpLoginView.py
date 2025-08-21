import random
import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import uuid

from ..serializers.otpLoginSerializer import RequestOTPSerializer, VerifyOTPSerializer
from redis_client import redis_client


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']
            otp = f"{random.randint(100000, 999999)}"

            redis_client.setex(f"otp:{user.account_id}", 300, otp)

            if user.email:
                # Render your HTML
                unique_token = str(uuid.uuid4())  # makes email unique
                html_message = render_to_string('emails/otp_email.html', {
                    'name': user.name,
                    'otp': otp,
                    'unique_token': unique_token,
                })

                text_message = f"Your OTP code is: {otp}"

                subject = f"Your OTP Code {otp}"  # subject unique too
                from_email = "astheshriketoyoursharp@gmail.com"
                to = [user.email]

                msg = EmailMultiAlternatives(subject, text_message, from_email, to)
                msg.attach_alternative(html_message, "text/html")

                # 🚀 Force Gmail to treat it as unique
                msg.extra_headers = {
                    "Message-ID": f"<{uuid.uuid4()}@volare.com>",
                    "References": "",
                    "In-Reply-To": "",
                }

                msg.send()
                return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

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

            self.cache_user_data(user)

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

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


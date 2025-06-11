from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers.paymentSerializer import ReservationPaymentSerializer, PaymentStatusSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import datetime


class ReservationPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id):
        serializer = ReservationPaymentSerializer(
            data=request.data,
            context={
                "reservation_id": reservation_id,
                "user_id": request.user.account_id
            }
        )
        if serializer.is_valid():
            result = serializer.save()
            subject = "Your Reservation is Confirmed"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [request.user.email]

            html_content = render_to_string("emails/reservation_confirmation.html", {
                **result,
                "current_year": datetime.datetime.now().year
            })
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id):
        serializer = PaymentStatusSerializer(data={}, context={
            "reservation_id": reservation_id,
            "user_id": request.user.account_id
        })
        if serializer.is_valid():
            result = serializer.get_status()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
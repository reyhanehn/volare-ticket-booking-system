from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin
from django.db import connection
from ..serializers.adminReservationSerializer import EditReservationSerializer, AdminConfirmReservationSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import datetime


class AdminEditReservationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, reservation_id):
        serializer = EditReservationSerializer(data=request.data, context={"reservation_id": reservation_id})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminConfirmReservationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, reservation_id):
        serializer = AdminConfirmReservationSerializer(data={}, context={"reservation_id": reservation_id})
        if serializer.is_valid():
            result = serializer.save()

            subject = "Your Reservation is Confirmed"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [result.pop("email")]

            html_content = render_to_string("emails/reservation_confirmation.html", {
                **result,
                "current_year": datetime.datetime.now().year
            })
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({"message": "Reservation confirmed and email sent.", **result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

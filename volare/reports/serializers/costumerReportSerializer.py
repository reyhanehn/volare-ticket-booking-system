from django.db import connection
from rest_framework import serializers
from accounts.models.account import Account
from ..models.report import ReportType


class CostumerReportSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=15, required=False)
    related_report = serializers.IntegerField()
    text = serializers.CharField()

    def validate(self, data):
        report_type = data["type"]
        valid_report_types = [ReportType.TICKET.value, ReportType.PAYMENT.value, ReportType.RESERVATION.value]
        related_report = data["related_report"]

        if not report_type in valid_report_types:
            raise serializers.ValidationError("Invalid report type")

        query_map = {
            ReportType.TICKET: "SELECT 1 FROM bookings_ticket WHERE ticket_id = %s",
            ReportType.PAYMENT: "SELECT 1 FROM bookings_payment WHERE payment_id = %s",
            ReportType.RESERVATION: "SELECT 1 FROM bookings_reservation WHERE reservation_id = %s",
        }


        query = query_map.get(report_type)
        if not query:
            raise serializers.ValidationError("Invalid report type.")

        with connection.cursor() as cursor:
            cursor.execute(query, [related_report])
            if not cursor.fetchone():
                raise serializers.ValidationError(f"{report_type} not found.")

        return data

    def create(self, validated_data):
        account_id = self.context['request'].user.account_id
        with connection.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO reports_report
                           (account_id, status, text, type, related_report_id)
                           VALUES (%s, 'Pending', %s, %s, %s)
                           RETURNING report_id
                           """, [
                               account_id,
                               validated_data['text'],
                               validated_data['type'],
                               validated_data['related_report']
                           ])
            report_id = cursor.fetchone()[0]
        return {
            "report_id": report_id,
            **validated_data,
            "status": "Pending",
        }


class ListMyReportsSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    admin = serializers.IntegerField(allow_null=True)
    status = serializers.CharField()
    text = serializers.CharField()
    answer = serializers.CharField(allow_null=True)
    type = serializers.CharField()
    related_report = serializers.IntegerField()

    @classmethod
    def get_reports(cls, account_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT report_id, admin_id, status, text, answer, type, related_report
                FROM reports_report
                WHERE account_id = %s
            """, [account_id])
            rows = cursor.fetchall()

        data = [
            {
                "report_id": row[0],
                "admin": row[1],
                "status": row[2],
                "text": row[3],
                "answer": row[4],
                "type": row[5],
                "related_report": row[6],
            }
            for row in rows
        ]
        return cls(data, many=True).data

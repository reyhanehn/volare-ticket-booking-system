from django.db import connection
from rest_framework import serializers
from accounts.models.account import Account
from ..models.report import ReportType, ReportStatus


class CustomerReportSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=15, required=False)
    related_report = serializers.IntegerField()
    text = serializers.CharField()

    def validate(self, data):
        report_type = data["type"]
        related_report = data["related_report"]

        valid_report_types = [
            ReportType.TICKET.value,
            ReportType.PAYMENT.value,
            ReportType.RESERVATION.value
        ]

        if report_type not in valid_report_types:
            raise serializers.ValidationError("Invalid report type")

        query_map = {
            ReportType.TICKET.value: "SELECT ticket_id FROM bookings_ticket WHERE ticket_id = %s",
            ReportType.PAYMENT.value: """
                SELECT t.ticket_id
                FROM bookings_payment p
                JOIN bookings_reservation r ON p.reservation_id = r.reservation_id
                JOIN bookings_ticket t ON t.ticket_id = r.ticket_id
                WHERE p.payment_id = %s
            """,
            ReportType.RESERVATION.value: """
                SELECT t.ticket_id
                FROM bookings_reservation r
                JOIN bookings_ticket t ON t.ticket_id = r.ticket_id
                WHERE r.reservation_id = %s
            """,
        }

        query = query_map.get(report_type)
        with connection.cursor() as cursor:
            cursor.execute(query, [related_report])
            row = cursor.fetchone()
            if not row:
                raise serializers.ValidationError(f"{report_type} not found.")
            data["related_report"] = row[0]  # Overwrite with ticket_id

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
    status = serializers.ChoiceField(required=False, choices=ReportStatus)
    type = serializers.ChoiceField(required=False, choices=ReportType)

    def get_reports(self, account_id):
        filters = self.validated_data

        params = [account_id]

        sql = """
                SELECT report_id, admin_id, status, text, answer, type, related_report_id
                FROM reports_report
                WHERE account_id = %s
            """

        if "status" in filters:
            sql += " AND status = %s"
            params.append(filters['status'])

        if "type" in filters:
            sql += " AND type = %s"
            params.append(filters['type'])

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        result = [
            {
                "report_id": row[0],
                "admin": row[1],
                "status": row[2],
                "text": row[3],
                "answer": row[4],
                "type": row[5],
                "related_report_id": row[6],
            }
            for row in rows
        ]
        return result

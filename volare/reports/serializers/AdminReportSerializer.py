from django.db import connection
from rest_framework import serializers
from accounts.models.account import Account
from ..models.report import ReportType, ReportStatus


class AnswerReportSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    answer = serializers.CharField()

    def save(self):
        admin_id = self.context['request'].user.account_id
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE reports_report
                SET admin_id = %s, status = 'Checked', answer = %s
                WHERE report_id = %s
            """, [
                admin_id,
                self.validated_data['answer'],
                self.validated_data['report_id']
            ])
        return self.validated_data


class SearchReportsSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(required=False)
    admin_id = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(required=False, choices=ReportStatus)
    type = serializers.ChoiceField(required=False, choices=ReportType)
    related_report = serializers.IntegerField(required=False)

    def get_reports(self):
        filters = self.validated_data

        params = []

        sql = """
                SELECT report_id, account_id, admin_id, status, text, answer, type, related_report_id
                FROM reports_report
                WHERE 1=1
            """

        if "status" in filters:
            sql += " AND status = %s"
            params.append(filters['status'])

        if "type" in filters:
            sql += " AND type = %s"
            params.append(filters['type'])

        if "account_id" in filters:
            sql += " AND account_id = %s"
            params.append(filters['account_id'])

        if "admin_id" in filters:
            sql += " AND admin_id = %s"
            params.append(filters['admin_id'])

        if "related_report" in filters:
            sql += " AND related_report_id = %s"
            params.append(filters['related_report'])

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        result = [
            {
                "report_id": row[0],
                "account": row[1],
                "admin": row[2],
                "status": row[3],
                "text": row[4],
                "answer": row[5],
                "type": row[6],
                "related_report_id": row[7],
            }
            for row in rows
        ]
        return result


class ViewReportSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()

    def get_report(self):
        report_id = self.validated_data["report_id"]

        sql = """
                SELECT report_id, account_id, admin_id, status, text, answer, type, related_report_id
                FROM reports_report
                WHERE report_id = %s
            """

        with connection.cursor() as cursor:
            cursor.execute(sql, [report_id])
            row = cursor.fetchone()

        if row is None:
            raise serializers.ValidationError("Report not found")

        return {
            "report_id": row[0],
            "account": row[1],
            "admin": row[2],
            "status": row[3],
            "text": row[4],
            "answer": row[5],
            "type": row[6],
            "related_report_id": row[7],
        }



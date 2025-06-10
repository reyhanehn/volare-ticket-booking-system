from rest_framework import serializers
from django.db import connection
from accounts.models.account import AccountRole


class PaymentHistorySerializer(serializers.Serializer):
    method = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)

    def get_history(self):
        user_id = self.context["user_id"]
        filters = self.validated_data
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT account_id, role FROM account WHERE account_id = %s
            """, [user_id])
            row = cursor.fetchone()
        if not row:
            raise serializers.ValidationError("User doesn't exist")
        role = row[1]

        sql = '''
            SELECT p.reservation_id, p.amount, p.payment_method, p.status, p.payment_date, p.payment_time,
            a.name, a.lastname
            FROM bookings_payment p
            JOIN account a on p.account_id = a.account_id
            WHERE 1 = 1
        '''
        params = list()

        if "method" in filters:
            sql += " AND payment_method = %s"
            params.append(filters["method"])

        if "status" in filters:
            sql += " AND status = %s"
            params.append(filters["status"])

        if "start_date" in filters:
            sql += " AND payment_date >= %s"
            params.append(filters["start_date"])

        if "end_date" in filters:
            sql += " AND payment_date <= %s"
            params.append(filters["end_date"])

        if "start_time" in filters:
            sql += " AND payment_time >= %s"
            params.append(filters["start_time"])

        if "end_time" in filters:
            sql += " AND payment_time <= %s"
            params.append(filters["end_time"])

        if role == AccountRole.CUSTOMER.value:
            sql += " AND a.account_id = %s"
            params.append(user_id)
            if "account_id" in filters and filters["account_id"] != user_id:
                raise serializers.ValidationError("Customers can't access others payment history")

        elif "account_id" in filters and role == AccountRole.ADMIN.value:
            sql += " AND a.account_id = %s"
            params.append(filters["account_id"])

        if role == AccountRole.COMPANY_ADMIN.value:
            raise serializers.ValidationError("Company admins can't access payment history")

        order = filters.get("order", "DESC").upper()
        if order not in ["ASC", "DESC"]:
            order = "DESC"

        sql += f" ORDER BY payment_date {order}, payment_time {order}"

        results = []
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            for row in rows:
                payment_info = {
                    "reservation_id": row[0],
                    "amount": row[1],
                    "method": row[2],
                    "status": row[3],
                    "date": row[4],
                    "time": str(row[5])
                }
                if role == AccountRole.ADMIN.value:
                    user_fullname = row[6] + " " + row[7]
                    payment_info["user info"] = user_fullname
                results.append(payment_info)

        return results

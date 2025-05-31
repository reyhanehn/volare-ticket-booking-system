from rest_framework import serializers
from django.db import connection
from decimal import Decimal

from ..models.wallet_transactions import WalletTransaction


class WalletTransactionListSerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField()
    wallet_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    type = serializers.CharField()
    transaction_date = serializers.DateField()
    transaction_time = serializers.TimeField()

    @classmethod
    def get_transactions(cls, user, transaction_type=None):
        with connection.cursor() as cursor:
            # Fetch wallet_id
            cursor.execute("SELECT wallet_id FROM wallet WHERE account_id = %s", [user.account_id])
            result = cursor.fetchone()
            if not result:
                raise serializers.ValidationError("Wallet not found.")
            wallet_id = result[0]
            # Fetch transactions
            if transaction_type:
                cursor.execute("""
                    SELECT transaction_id, wallet_id, amount, type, transaction_date, transaction_time, related_payment_id_id
                    FROM wallet_transactions
                    WHERE wallet_id = %s AND type = %s
                    ORDER BY transaction_date DESC, transaction_time DESC
                """, [wallet_id, transaction_type])
            else:
                cursor.execute("""
                    SELECT transaction_id, wallet_id, amount, type, transaction_date, transaction_time, related_payment_id_id
                    FROM wallet_transactions
                    WHERE wallet_id = %s
                    ORDER BY transaction_date DESC, transaction_time DESC
                """, [wallet_id])

            rows = cursor.fetchall()

        transactions = [
            {
                'transaction_id': row[0],
                'wallet_id': row[1],
                'amount': row[2],
                'type': row[3],
                'transaction_date': row[4],
                'transaction_time': row[5],
                'related_payment_id' : row[6],
            }
            for row in rows
        ]
        return cls(transactions, many=True)



class WalletChargeSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    def save(self, **kwargs):
        amount = self.validated_data['amount']
        user = self.context['request'].user

        with connection.cursor() as cursor:
            # Fetch wallet
            cursor.execute("SELECT wallet_id, balance FROM wallet WHERE account_id = %s", [user.account_id])
            wallet_row = cursor.fetchone()
            if not wallet_row:
                raise serializers.ValidationError("Wallet not found.")

            wallet_id, balance = wallet_row
            new_balance = Decimal(str(balance)) + Decimal(amount)

            # Update wallet balance
            cursor.execute("UPDATE wallet SET balance = %s WHERE wallet_id = %s;", [new_balance, wallet_id])

            # Insert transaction
            cursor.execute("""
                INSERT INTO wallet_transactions (wallet_id, type, amount, transaction_date, transaction_time)
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME)
                RETURNING transaction_id, transaction_date,transaction_time;
            """, [wallet_id, 'Charge', amount])
            row = cursor.fetchone()
            transaction_id = row[0]

        transaction = WalletTransaction(
            wallet_id=wallet_id,
            transaction_id=transaction_id,
            amount=amount,
            type="Charge",
            transaction_date=row[1],
            transaction_time=row[2]
        )
        transaction._state.adding = False

        return transaction

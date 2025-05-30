from rest_framework import serializers
from django.db import connection
from decimal import Decimal

from ..models.wallet_transactions import WalletTransaction


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

from rest_framework import serializers
from django.db import connection


class WalletSerializer(serializers.Serializer):
    wallet_id = serializers.IntegerField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    charge_count = serializers.IntegerField()
    payment_count = serializers.IntegerField()
    refund_count = serializers.IntegerField()

    @classmethod
    def from_account(cls, account_id):
        with connection.cursor() as cursor:
            # Get wallet info
            cursor.execute("""
                SELECT wallet_id, balance 
                FROM wallet 
                WHERE account_id = %s
            """, [account_id])
            row = cursor.fetchone()
            if not row:
                raise Exception("Wallet not found.")
            wallet_id, balance = row

            # Get transaction counts
            cursor.execute("""
                SELECT type, COUNT(*) 
                FROM wallet_transactions 
                WHERE wallet_id = %s 
                GROUP BY type
            """, [wallet_id])
            tx_counts = dict(cursor.fetchall())
            # Normalize all 3 types
            data = {
                'wallet_id': wallet_id,
                'balance': balance,
                'charge_count': tx_counts.get('CHARGE', 0),
                'payment_count': tx_counts.get('PAYMENT', 0),
                'refund_count': tx_counts.get('REFUND', 0),
            }
            return cls(data)

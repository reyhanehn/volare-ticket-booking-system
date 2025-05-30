from django.db import models
from django.utils import timezone
from .wallet import Wallet


class TransactionType(models.TextChoices):
    CHARGE = 'Charge'
    PAYMENT = 'Payment'
    REFUND = 'Refund'


class WalletTransaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    related_payment_id = models.ForeignKey('payments.Payment', null=True, blank=True, unique=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    transaction_date = models.DateField(default=timezone.now)
    transaction_time = models.TimeField(default=timezone.now)

    class Meta:
        db_table = 'wallet_transactions'

    def __str__(self):
        return f'Transaction {self.transaction_id} ({self.type}) for Wallet {self.wallet.wallet_id}'
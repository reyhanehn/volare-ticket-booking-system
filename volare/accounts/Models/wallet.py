from django.db import models
from volare.accounts.Models import Account


class Wallet(models.Model):
    wallet_id = models.BigAutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'wallet'

    def __str__(self):
        return f'Wallet {self.wallet_id} for Account {self.account} with balance {self.balance}'
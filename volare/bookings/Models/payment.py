from django.db import models
from .reservation import Reservation


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = 'Credit Card'
    PAYPAL = 'PayPal'
    BANK_TRANSFER = 'Bank Transfer'
    CASH = 'Cash'
    WALLET = 'Wallet'


class PaymentStatus(models.TextChoices):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    REFUNDED = 'Refunded'


class Payment(models.Model):
    payment_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='payments')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_time = models.TimeField(auto_now_add=True)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
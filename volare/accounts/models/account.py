from django.db import models
from django.utils import timezone


# Enums as Django choices
class AccountRole(models.TextChoices):
    CUSTOMER = 'Customer'
    ADMIN = 'Admin'
    COMPANY_OWNER = 'Company_Owner'


class AccountStatus(models.TextChoices):
    ACTIVE = 'Active'
    BANNED = 'Banned'


class Account(models.Model):
    account_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=AccountRole.choices)
    status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    password_hash = models.TextField()
    city = models.ForeignKey('bookings.Location', null=True, blank=True, on_delete=models.SET_NULL)
    registration_date = models.DateField(default=timezone.now)
    birthdate = models.DateField(null=True, blank=True)

    @property
    def id(self):
        return self.account_id

    class Meta:
        db_table = 'account'

    def __str__(self):
        return f'{self.name} {self.lastname} ({self.role})'

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError


# Enums as Django choices
class AccountRole(models.TextChoices):
    CUSTOMER = 'Customer'
    ADMIN = 'Admin'
    COMPANY_OWNER = 'Company_Owner'


class AccountStatus(models.TextChoices):
    ACTIVE = 'Active'
    BANNED = 'Banned'


class AccountManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Users must have either an email address or phone number.')

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', AccountRole.ADMIN)
        extra_fields.setdefault('status', AccountStatus.ACTIVE)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('Superuser must have an email address.')

        return self.create_user(email=email, password=password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    account_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=AccountRole.choices)
    status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)

    city = models.ForeignKey('bookings.Location', null=True, blank=True, on_delete=models.SET_NULL)
    registration_date = models.DateField(default=timezone.now)
    birth_date = models.DateField(null=True, blank=True)

    # This field is required by Django's auth system
    last_login = models.DateTimeField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)  # for admin site access

    # Remove default is_active field and replace with property below
    # is_active will be derived from status field

    password_hash = models.CharField(max_length=128)  # Your stored password column

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            raise ValidationError('Either email or phone number must be set.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    # Override password field to use your password_hash column
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password_hash = make_password(raw_password)

    # Alias for Django's 'date_joined' attribute
    @property
    def date_joined(self):
        return self.registration_date

    # Override is_active to reflect your status field
    @property
    def is_active(self):
        return self.status == AccountStatus.ACTIVE

    @is_active.setter
    def is_active(self, value):
        self.status = AccountStatus.ACTIVE if value else AccountStatus.BANNED

    class Meta:
        db_table = 'account'

    def __str__(self):
        return f'{self.name} {self.lastname} ({self.role})'

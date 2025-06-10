from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from ..models.passenger import Passenger
from ..models.ticket import Ticket

EXPIRATION_DURATION_MINUTES = 1

class ReservationStatus(models.TextChoices):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'

def default_expiration_time():
    return timezone.now() + timedelta(minutes=10)

class Reservation(models.Model):
    reservation_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='reservations')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='reservations')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reservations')
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    reservation_date = models.DateField(auto_now_add=True)
    reservation_time = models.TimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(default=default_expiration_time)
    cancelled_by = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_reservations')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ticket", "seat_number"],
                condition=~Q(status=ReservationStatus.CANCELLED),
                name="unique_active_seat"
            )
        ]

    def __str__(self):
        return f"Reservation {self.reservation_id} - Seat {self.seat_number}"

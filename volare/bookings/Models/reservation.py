from django.db import models

from volare.bookings.Models.passenger import Passenger
from volare.bookings.Models.ticket import Ticket


class ReservationStatus(models.TextChoices):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'


class Reservation(models.Model):
    reservation_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='reservations')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='reservations')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reservations')
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    reservation_date = models.DateField(auto_now_add=True)
    reservation_time = models.TimeField(auto_now_add=True)
    expiration = models.DurationField()
    cancelled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cancelled_reservations')

    class Meta:
        unique_together = ('ticket', 'seat_number')

    def __str__(self):
        return f"Reservation {self.reservation_id} - Seat {self.seat_number}"
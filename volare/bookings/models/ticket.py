from django.db import models

from ..models.location import Station
from ..models.route import Route


class StopType(models.TextChoices):
    TRANSIT = 'Transit'
    MEAL = 'Meal'
    REFUEL = 'Refuel'
    LAYOVER = 'Layover'


class Trip(models.Model):
    trip_id = models.BigAutoField(primary_key=True)
    vehicle = models.ForeignKey('companies.Vehicle', on_delete=models.CASCADE, related_name='trips')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    departure_datetime = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Trip {self.trip_id} on {self.departure_datetime}"


class Ticket(models.Model):
    ticket_id = models.BigAutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    section = models.ForeignKey('companies.VehicleSection', on_delete=models.CASCADE, related_name='tickets')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_seats = models.PositiveSmallIntegerField(default=0)
    seat_start_number = models.PositiveSmallIntegerField(default=0)
    seat_end_number = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Ticket {self.ticket_id} for Trip {self.trip if self.trip else 'N/A'}"


class TripStop(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    stop_order = models.PositiveSmallIntegerField()
    stop_type = models.CharField(max_length=10, choices=StopType.choices)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        unique_together = ('trip', 'stop_order')
        ordering = ['stop_order']

    def __str__(self):
        return f"Stop {self.stop_order} on Trip {self.trip}"
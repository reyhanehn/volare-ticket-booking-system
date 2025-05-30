from django.db import models

from ..models.company import Company


class TransportType(models.TextChoices):
    TRAIN = 'Train'
    BUS = 'Bus'
    AIRPLANE = 'Airplane'


class Vehicle(models.Model):
    vehicle_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vehicles')
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TransportType.choices)
    class_code = models.PositiveSmallIntegerField()  # 1 to 5 constraint should be validated in app logic/forms
    total_seats = models.PositiveIntegerField()  # seats > 0 enforced by PositiveIntegerField
    layout = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name or 'Unnamed Vehicle'} ({self.type})"


class VehicleSection(models.Model):
    section_id = models.BigAutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=20, blank=True, null=True)
    seats_count = models.PositiveIntegerField()  # seats > 0

    def __str__(self):
        return f"{self.name or 'Section'} of Vehicle {self.vehicle}"

from django.db import models
from volare.companies.Models.vehicle import Vehicle


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class VehicleService(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('vehicle', 'service')

    def __str__(self):
        return f"Service '{self.service.name}' for Vehicle {self.vehicle.vehicle_id}"
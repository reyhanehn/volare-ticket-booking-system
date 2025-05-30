from django.db import models
from ..models.location import Location, Station


class Route(models.Model):
    route_id = models.BigAutoField(primary_key=True)
    origin = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='routes_from')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='routes_to')
    origin_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes_origin', null=True, blank=True)
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='routes_destination', null=True, blank=True)

    def __str__(self):
        return f"Route from {self.origin} to {self.destination}"

    def clean(self):
        # Optional: Enforce origin != destination logic here if needed in app validation
        if self.origin == self.destination:
            raise ValidationError("Origin and Destination must be different.")
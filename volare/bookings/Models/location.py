from django.db import models


class StationType(models.TextChoices):
    TRAIN_STATION = 'Train_Station', 'Train Station'
    BUS_STATION = 'Bus_Station', 'Bus Station'
    AIRPORT = 'Airport', 'Airport'


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    class Meta:
        unique_together = ('country', 'city')

    def __str__(self):
        return f"{self.city}, {self.country}"


class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)  # no enum provided for station_type, so plain CharField
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stations')

    class Meta:
        unique_together = ('name', 'location')

    def __str__(self):
        return self.name
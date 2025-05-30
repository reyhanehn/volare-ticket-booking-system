from django.db import models


class Passenger(models.Model):
    passenger_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    ssn = models.CharField(max_length=10, unique=True, null=True, blank=True)
    birthdate = models.DateField()
    picture_url = models.TextField(null=True, blank=True)
    related_account = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, null=True, blank=True, related_name='passengers')

    def __str__(self):
        return f"{self.name} {self.lastname}"
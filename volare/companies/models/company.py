from django.db import models


class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    owner = models.OneToOneField(
        'accounts.Account',  # or 'accounts.Account' if not using custom user model
        on_delete=models.CASCADE,
        related_name='owned_companies'
    )
    name = models.CharField(max_length=50, unique=True)
    logo_url = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # numeric

    def __str__(self):
        return self.name
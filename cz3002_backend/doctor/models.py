from django.db import models

from authentication.models import User
from patient.models import Patient


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    working_address = models.CharField(max_length=255, null=True, blank=True)
    watchlist = models.ManyToManyField(Patient)

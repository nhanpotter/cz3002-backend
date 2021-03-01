from django.db import models
from cz3002_backend.authentication.models import User


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

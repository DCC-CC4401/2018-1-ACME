from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    esAdmin = models.BooleanField(default=False)

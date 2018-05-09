from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.datetime_safe import datetime

from customAuth.models import CustomUser


def get_time():
    return datetime.now().time()


def get_date():
    return datetime.now().date()


class Reserva(models.Model):
    nombreItem = models.CharField(max_length=100)
    horaInicio = models.TimeField(default=get_time)
    horaTermino = models.TimeField(default=get_time)
    solicitante = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    fechaReserva = models.DateField(default=get_date)
    fechaCreacion = models.DateTimeField(default=datetime.now)


class Prestamo(models.Model):
    nombreItem = models.CharField(max_length=100)
    horaInicio = models.TimeField(default=get_time)
    horaTermino = models.TimeField(default=get_time)
    solicitante = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    fechaPrestamo = models.DateField(default=get_date)
    estado = (('V', 'Vigente'), ('P', 'Perdido'), ('C', 'Caducado'))


class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    estado = (('D', 'Disponible'), ('P', 'En prestamo'), ('R', 'En reparacion'), ('P', 'Perdido'))
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField(null=True)


class Espacio(models.Model):
    nombre = models.CharField(max_length=50)
    estado = (('D', 'Disponible'), ('P', 'En prestamo'), ('R', 'En reparacion'))
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField(null=True)
    capacidad = models.PositiveIntegerField(default=0)

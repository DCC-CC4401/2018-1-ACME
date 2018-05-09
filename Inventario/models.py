from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from customAuth.models import CustomUser


class Reserva(models.Model):
    nombreItem = models.CharField(max_length=100)
    horaInicio = models.TimeField
    horaTermino = models.TimeField
    solicitante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fechaReserva = models.DateField
    fechaCreacion = models.DateTimeField


class Prestamo(models.Model):
    nombreItem = models.CharField(max_length=100)
    horaInicio = models.TimeField
    horaTermino = models.TimeField
    solicitante = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fechaPrestamo = models.DateField
    estado = (('V', 'Vigente'), ('P', 'Perdido'), ('C', 'Caducado'))


class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    estado = (('D', 'Disponible'), ('P', 'En prestamo'), ('R', 'En reparacion'), ('P', 'Perdido'))
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField


class Espacio(models.Model):
    nombre = models.CharField(max_length=50)
    estado = (('D', 'Disponible'), ('P', 'En prestamo'), ('R', 'En reparacion'))
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField
    capacidad = models.PositiveIntegerField

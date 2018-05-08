from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from customAuth.models import CustomUser


class Reserva(models.Model):
    id = models.PositiveIntegerField
    nombre = models.CharField(max_length=100)
    horaInicio = models.TimeField
    horaTermino = models.TimeField
    solicitante = CustomUser
    fechaReserva = models.DateField
    fechaCreacion = models.DateTimeField


class Prestamo(models.Model):
    id = models.PositiveIntegerField
    nombre = models.CharField(max_length=100)
    horaInicio = models.TimeField
    horaTermino = models.TimeField
    solicitante = CustomUser
    fechaPrestamo = models.DateField
    estado = (('V', 'Vigente'), ('P', 'Perdido'), ('C', 'Caducado'))


class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    nameId = models.CharField(max_length=100)
    estado = (('D', 'Disponible'), ('P', 'En prestamo'), ('R', 'En reparacion'), ('P', 'Perdido'))
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField


class Espacio(models.Model):
    nombre = models.CharField(max_length=50)
    nameId = models.CharField(max_length=100)
    estado = (('D', 'Disponible'), ('P', 'En prestamo'), ('R', 'En reparacion'))
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField
    capacidad = models.PositiveIntegerField

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=10)
    correo = models.EmailField(max_length=60)
    password = models.CharField(max_length=200)
    esAdmin = models.BooleanField


class Reserva(models.Model):
    id = models.PositiveIntegerField
    nombre = models.CharField(max_length=100)
    horaInicio = models.TimeField
    horaTermino = models.TimeField
    solicitante = Usuario
    fechaReserva = models.DateField
    fechaCreacion = models.DateTimeField


class Prestamo(models.Model):
    id = models.PositiveIntegerField
    nombre = models.CharField(max_length=100)
    horaInicio = models.TimeField
    horaTermino = models.TimeField
    solicitante = Usuario
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

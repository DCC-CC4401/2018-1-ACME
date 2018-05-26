from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.datetime_safe import datetime

from customAuth.models import CustomUser


def get_time():
    return datetime.now().time()


def get_date():
    return datetime.now().date()


class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField(upload_to='static/imgarticulo/', default='imgarticulo/None/no-img.jpg')


class Espacio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField(null=True)
    capacidad = models.PositiveIntegerField(default=0)


class Reserva(models.Model):
    horaInicio = models.TimeField(default=get_time)
    horaTermino = models.TimeField(default=get_time)
    solicitante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, null=True)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, null=True)
    fechaReserva = models.DateField(default=get_date)
    fechaCreacion = models.DateTimeField(default=datetime.now)


class Prestamo(models.Model):
    nombreItem = models.CharField(max_length=100)
    horaInicio = models.TimeField(default=get_time)
    horaTermino = models.TimeField(default=get_time)
    solicitante = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, null=True)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, null=True)
    fechaPrestamo = models.DateField(default=get_date)


class EstadoReserva(models.Model):
    PROCESO = 'P'
    ACEPTADO = 'A'
    RECHAZADO = 'R'
    ESTADO_CHOICES = (
        (PROCESO, 'En Proceso'),
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    )
    fecha = models.DateTimeField(default=datetime.now)
    estado = models.CharField(max_length=1,
                              choices=ESTADO_CHOICES,
                              default=PROCESO)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True)

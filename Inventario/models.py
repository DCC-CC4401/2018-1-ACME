from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.datetime_safe import datetime

HABILITADO = 'H'
INHABILITADO = 'I'
PENDIENTE = 'P'
ENTREGADO = 'E'
RECHAZADO = 'R'
RECIBIDO = 'C'
PERDIDO = 'D'
DISPONIBLE = 'S'
PRESTAMO = 'M'
REPARACION = 'A'

ESTADOS_USUARIO = (
    (HABILITADO, 'Habilitado'),
    (INHABILITADO, 'Inhabilitado'),
)

ESTADOS_RESERVA = (
    (PENDIENTE, 'Pendiente'),
    (ENTREGADO, 'Entregado'),
    (RECHAZADO, 'Rechazado'),
)

ESTADOS_PRESTAMO = (
    (PENDIENTE, 'Pendiente'),
    (RECIBIDO, 'Recibido'),
    (PERDIDO, 'Perdido'),
)

ESTADOS_ARTICULO = (
    (DISPONIBLE, 'Disponible'),
    (PRESTAMO, 'En Préstamo'),
    (REPARACION, 'En Reparación'),
    (PERDIDO, 'Perdido'),
)

ESTADOS_ESPACIO = (
    (DISPONIBLE, 'Disponible'),
    (PRESTAMO, 'En Préstamo'),
    (REPARACION, 'En Reparación'),
)


def get_time():
    return datetime.now().time()


def get_date():
    return datetime.now().date()


def in_estados(estados, check):
    for estado, _ in estados:
        if estado == check:
            return True
    return False


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    apellido = models.CharField(max_length=30, verbose_name='Apellido')
    esAdmin = models.BooleanField(default=False, verbose_name='Administrador')
    estado = models.CharField(max_length=1, choices=ESTADOS_USUARIO, default=HABILITADO, verbose_name='Estado')
    email = models.EmailField(max_length=80, verbose_name='Email', unique=True)

    def get_code(self):
        return 'U' + str(self.id)

    def __str__(self):
        return self.nombre + ' ' + self.apellido + ' ' + self.email + ' [' + self.get_code() + ']'


class Articulo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    descripcion = models.CharField(max_length=500, verbose_name='Descripción')
    foto = models.ImageField(upload_to='static/imgarticulo/', default='imgarticulo/None/no-img.jpg',
                             verbose_name='Foto')
    estado = models.CharField(max_length=1, choices=ESTADOS_ARTICULO, default=DISPONIBLE, verbose_name='Estado')

    def get_code(self):
        return 'A' + str(self.id)

    def __str__(self):
        return self.nombre + ' [' + self.get_code() + ']'


class Espacio(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    descripcion = models.CharField(max_length=500, verbose_name='Descripción')
    foto = models.ImageField(upload_to='static/imgespacio/', default='imgespacio/None/no-img.jpg',
                             verbose_name='Foto')
    capacidad = models.PositiveIntegerField(default=0, verbose_name='Capacidad')
    estado = models.CharField(max_length=1, choices=ESTADOS_ESPACIO, default=DISPONIBLE, verbose_name='Estado')

    def get_code(self):
        return 'E' + str(self.id)

    def __str__(self):
        return self.nombre + ' [' + self.get_code() + ']'


class Reserva(models.Model):
    horaInicio = models.TimeField(default=get_time, verbose_name='Hora de Inicio')
    horaTermino = models.TimeField(default=get_time, verbose_name='Hora de Término')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Solicitante')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Artículo')
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Espacio')
    fechaReserva = models.DateField(default=get_date, verbose_name='Fecha de Reserva')
    fechaCreacion = models.DateTimeField(default=datetime.now, verbose_name='Fecha de Creación')
    estado = models.CharField(max_length=1, choices=ESTADOS_RESERVA, default=PENDIENTE, verbose_name='Estado')

    def get_code(self):
        return 'R' + str(self.id)

    def __str__(self):
        if self.articulo is not None:
            return self.solicitante.email + ' reserva ' + self.articulo.nombre + ' [' + self.get_code() + ']'
        else:
            return self.solicitante.email + ' reserva ' + self.espacio.nombre + ' [' + self.get_code() + ']'


class Prestamo(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, verbose_name='Reserva')
    fechaPrestamo = models.DateField(default=get_date, verbose_name='Fecha de Creación')
    estado = models.CharField(max_length=1, choices=ESTADOS_PRESTAMO, default=PENDIENTE, verbose_name='Estado')

    def get_code(self):
        return 'P' + str(self.id)

    def __str__(self):
        return 'Préstamo (' + str(self.reserva) + ')' + ' [' + self.get_code() + ']'


class EstadoReserva(models.Model):
    fecha = models.DateTimeField(default=datetime.now)
    estado = models.CharField(max_length=1, choices=ESTADOS_RESERVA, default=PENDIENTE)
    reserva_asociada = models.ForeignKey(Reserva, on_delete=models.CASCADE)

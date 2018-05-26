from django.contrib import admin

# Register your models here.
from Inventario.models import Espacio, Articulo, Prestamo, Reserva, EstadoReserva

admin.site.register(Reserva)
admin.site.register(Prestamo)
admin.site.register(Articulo)
admin.site.register(Espacio)
admin.site.register(EstadoReserva)

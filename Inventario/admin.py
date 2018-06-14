from django.contrib import admin

# Register your models here.
from Inventario.models import Espacio, Articulo, Prestamo, Reserva, RegistroEstadoReserva, RegistroEstadoPrestamo

admin.site.register(Reserva)
admin.site.register(Prestamo)
admin.site.register(Articulo)
admin.site.register(Espacio)
admin.site.register(RegistroEstadoReserva)
admin.site.register(RegistroEstadoPrestamo)

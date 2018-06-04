from django import template

register = template.Library()


@register.filter(name='nombreItem')
def nombreItem(reserva):
    nombre = ''
    if reserva.articulo is not None:
        nombre = reserva.articulo.nombre
    elif reserva.espacio is not None:
        nombre = reserva.espacio.nombre
    return nombre

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime, timedelta, date

from Inventario.models import Reserva, Prestamo


def index(request):
    if request.user.is_authenticated:
        if request.user.esAdmin:
            return landingPageAdministrador(request)
        else:
            return landingPageUsuario(request)
    else:
        return HttpResponseRedirect(reverse('customAuth:login'))


def landingPageUsuario(request):
    context = {}
    return render(request, 'Inventario/landingPageUsuario.html', context)


def landingPageAdministrador(request):
    reservas = Reserva.objects.order_by('-fechaReserva')
    prestamos = Prestamo.objects.order_by('-fechaPrestamo')
    lunes = (date.today() - timedelta(date.today().isoweekday()-1))
    domingo = (date.today() + timedelta(7-date.today().isoweekday()))
    reservagrilla = Reserva.objects.filter(fechaReserva__range=[lunes,domingo])
    context = {
        'reservas': reservas,
        'prestamos': prestamos,
        'lunes': lunes,
        'domingo': domingo,
        'reservagrilla': reservagrilla
    }
    return render(request, 'Inventario/landingPageAdministrador.html', context)


def perfilUsuario(request):
    if not request.user.is_authenticated or request.user.esAdmin:
        return HttpResponseRedirect(reverse('Inventario:index'))
    reservas = Reserva.objects.filter(solicitante=request.user)
    prestamos = Prestamo.objects.filter(solicitante=request.user)
    context = {
        'reservas': reservas,
        'prestamos': prestamos,
    }
    return render(request, 'Inventario/perfilUsuario.html', context)


def fichaArticulo(request, articuloId):
    context = {}
    return render(request, 'Inventario/fichaArticulo.html', context)

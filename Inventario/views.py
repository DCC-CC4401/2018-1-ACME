# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
    context = {}
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

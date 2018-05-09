# Create your views here.
import django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Inventario.models import Reserva, Prestamo
from customAuth.forms import RegistrationForm


def index(request):
    if request.user.is_authenticated:
        if request.user.esAdmin:
            return landingPageAdministrador(request)
        else:
            return landingPageUsuario(request)
    else:
        return django.contrib.auth.views.login(request)


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


def registrar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Inventario:index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Inventario:index'))
    form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

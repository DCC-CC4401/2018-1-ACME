# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime, timedelta, date

from Inventario.models import Reserva, Prestamo, Articulo, Espacio


def index(request):
    if request.user.is_authenticated:
        if request.user.esAdmin:
            return landingPageAdministrador(request)
        else:
            return landingPageUsuario(request)
    else:
        return HttpResponseRedirect(reverse('customAuth:login'))


def busquedaArticulos(request):
    q = request.GET.get('q', '')
    articulo = Articulo.objects.filter(nombre__icontains=q)
    return render(request, 'Inventario/landingPageUsuario.html', {'articulo': articulo})


def landingPageUsuario(request):
    articulos = Articulo.objects
    espacios = Espacio.objects
    reservas = Reserva.objects
    context = {
        'articulos': articulos,
        'espacios': espacios,
        'reservas': reservas,
    }
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
    reservas = Reserva.objects.order_by('-fechaReserva')
    articulo = Articulo.objects

    context = {
        'reservas': reservas,
        'articulo': articulo,
    }
    return render(request, 'Inventario/fichaArticulo.html', context)

def upload_img(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Articulo.objects.get(pk=course_id)
            m.foto = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')
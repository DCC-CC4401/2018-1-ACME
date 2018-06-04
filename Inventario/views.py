# Create your views here.
from datetime import timedelta, date

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve

from Inventario.forms import ReservaForm
from Inventario.models import Reserva, Prestamo, Articulo, Espacio, EstadoReserva


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
    lunes = (date.today() - timedelta(date.today().isoweekday() - 1))
    domingo = (date.today() + timedelta(7 - date.today().isoweekday()))
    reservagrilla = Reserva.objects.filter(fechaReserva__range=[lunes, domingo])
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

    context = {}

    if request.method == 'POST':
        count = 0
        list = request.POST.getlist('lista')
        for id in list:
            try:
                Reserva.objects.get(id=id, solicitante=request.user).delete()
                count += 1
            except Reserva.DoesNotExist:
                pass

        if count != len(list):
            context['alerta'] = 'Hubo un problema con la solicitud, se eliminaron {0} de {1} Reservas'.format(
                str(count), str(len(list)))
            context['tipoAlerta'] = 'error'
        else:
            context['alerta'] = 'Se eliminaron {0} Reservas'.format(str(count))
            context['tipoAlerta'] = 'success'

    reservas = Reserva.objects.filter(solicitante=request.user)
    prestamos = Prestamo.objects.filter(solicitante=request.user)
    context['reservas'] = reservas
    context['prestamos'] = prestamos
    context['PROCESO'] = EstadoReserva.PROCESO
    context['ACEPTADO'] = EstadoReserva.ACEPTADO
    context['RECHAZADO'] = EstadoReserva.RECHAZADO
    context['forma'] = ReservaForm()
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


def dbAPI(request):
    def getForm(dict):
        tipo = dict.get('tipo')
        if tipo == 'Reserva':
            return ReservaForm
        else:
            return None

    form = getForm(request.POST)
    redirect = request.POST.get('redirect', reverse('Inventario:index'))
    alerta = ''
    tipoAlerta = ''

    if request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

    request.method = 'GET'
    request.GET = {}
    response = resolve(redirect)
    response = response(request)
    if alerta != '':
        response.context_data['alerta'] = alerta
        response.context_data['tipoAlerta'] = tipoAlerta

    return response

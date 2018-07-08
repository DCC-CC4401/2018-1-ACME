# Create your views here.
from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from Inventario.forms import UsuarioForm, ReservaForm, PrestamoForm, ArticuloForm, EspacioForm, \
    CustomPasswordChangeForm, SimpleReservaForm
from Inventario.models import Reserva, Prestamo, Articulo, Espacio, Usuario, PENDIENTE, ENTREGADO, RECHAZADO, RECIBIDO, \
    PERDIDO, in_estados, ESTADOS_RESERVA, ESTADOS_PRESTAMO, RegistroEstadoReserva, RegistroEstadoPrestamo, DISPONIBLE, \
    PRESTAMO, REPARACION


def index(request):
    if request.user.is_authenticated:
        if request.user.esAdmin:
            return landingPageAdministrador(request)
        else:
            return landingPageUsuario(request)
    else:
        return redirect('customAuth:login')


def busquedaArticulos(request):
    context = {}
    if (request.GET.get('q', '')):
        q = request.GET.get('q', '')
        articulo = Articulo.objects.all().filter(nombre__icontains=q).order_by('nombre')
        context['articulos'] = articulo
    return render(request, 'Inventario/landingPageUsuario.html', context)


def landingPageUsuario(request):
    count = 0
    if (request.GET.get('count', '')):
        count = int(request.GET.get('count', ''))
    reservas = Reserva.objects.order_by('-fechaReserva').exclude(articulo__isnull=True).filter(estado='P')
    prestamos = Prestamo.objects.order_by('-fechaPrestamo')
    lunes = (date.today() - timedelta(date.today().isoweekday() - 1) + timedelta(7 * count))
    domingo = (date.today() + timedelta(7 - date.today().isoweekday()) + timedelta(7 * count))
    reservagrilla = Reserva.objects.filter(fechaReserva__range=[lunes, domingo]).exclude(espacio__isnull=True)
    reservalunes = reservagrilla.filter(fechaReserva__week_day=2)
    reservamartes = reservagrilla.filter(fechaReserva__week_day=3)
    reservamiercoles = reservagrilla.filter(fechaReserva__week_day=4)
    reservajueves = reservagrilla.filter(fechaReserva__week_day=5)
    reservaviernes = reservagrilla.filter(fechaReserva__week_day=6)
    reservasabado = reservagrilla.filter(fechaReserva__week_day=7)
    reservadomingo = reservagrilla.filter(fechaReserva__week_day=1)
    lunes1 = reservalunes.filter(horaInicio__hour=9)
    lunes2 = reservalunes.filter(horaInicio__hour=10)
    lunes3 = reservalunes.filter(horaInicio__hour=11)
    lunes4 = reservalunes.filter(horaInicio__hour=12)
    lunes5 = reservalunes.filter(horaInicio__hour=13)
    lunes6 = reservalunes.filter(horaInicio__hour=14)
    lunes7 = reservalunes.filter(horaInicio__hour=15)
    lunes8 = reservalunes.filter(horaInicio__hour=16)
    lunes9 = reservalunes.filter(horaInicio__hour=17)
    martes1 = reservamartes.filter(horaInicio__hour=9)
    martes2 = reservamartes.filter(horaInicio__hour=10)
    martes3 = reservamartes.filter(horaInicio__hour=11)
    martes4 = reservamartes.filter(horaInicio__hour=12)
    martes5 = reservamartes.filter(horaInicio__hour=13)
    martes6 = reservamartes.filter(horaInicio__hour=14)
    martes7 = reservamartes.filter(horaInicio__hour=15)
    martes8 = reservamartes.filter(horaInicio__hour=16)
    martes9 = reservamartes.filter(horaInicio__hour=17)
    miercoles1 = reservamiercoles.filter(horaInicio__hour=9)
    miercoles2 = reservamiercoles.filter(horaInicio__hour=10)
    miercoles3 = reservamiercoles.filter(horaInicio__hour=11)
    miercoles4 = reservamiercoles.filter(horaInicio__hour=12)
    miercoles5 = reservamiercoles.filter(horaInicio__hour=13)
    miercoles6 = reservamiercoles.filter(horaInicio__hour=14)
    miercoles7 = reservamiercoles.filter(horaInicio__hour=15)
    miercoles8 = reservamiercoles.filter(horaInicio__hour=16)
    miercoles9 = reservamiercoles.filter(horaInicio__hour=17)
    jueves1 = reservajueves.filter(horaInicio__hour=9)
    jueves2 = reservajueves.filter(horaInicio__hour=10)
    jueves3 = reservajueves.filter(horaInicio__hour=11)
    jueves4 = reservajueves.filter(horaInicio__hour=12)
    jueves5 = reservajueves.filter(horaInicio__hour=13)
    jueves6 = reservajueves.filter(horaInicio__hour=14)
    jueves7 = reservajueves.filter(horaInicio__hour=15)
    jueves8 = reservajueves.filter(horaInicio__hour=16)
    jueves9 = reservajueves.filter(horaInicio__hour=17)
    viernes1 = reservaviernes.filter(horaInicio__hour=9)
    viernes2 = reservaviernes.filter(horaInicio__hour=10)
    viernes3 = reservaviernes.filter(horaInicio__hour=11)
    viernes4 = reservaviernes.filter(horaInicio__hour=12)
    viernes5 = reservaviernes.filter(horaInicio__hour=13)
    viernes6 = reservaviernes.filter(horaInicio__hour=14)
    viernes7 = reservaviernes.filter(horaInicio__hour=15)
    viernes8 = reservaviernes.filter(horaInicio__hour=16)
    viernes9 = reservaviernes.filter(horaInicio__hour=17)
    viernes10 = reservaviernes.filter(horaInicio__hour=18)
    sabado1 = reservasabado.filter(horaInicio__hour=9)
    sabado2 = reservasabado.filter(horaInicio__hour=10)
    sabado3 = reservasabado.filter(horaInicio__hour=11)
    sabado4 = reservasabado.filter(horaInicio__hour=12)
    sabado5 = reservasabado.filter(horaInicio__hour=13)
    sabado6 = reservasabado.filter(horaInicio__hour=14)
    sabado7 = reservasabado.filter(horaInicio__hour=15)
    sabado8 = reservasabado.filter(horaInicio__hour=16)
    sabado9 = reservasabado.filter(horaInicio__hour=17)
    domingo1 = reservadomingo.filter(horaInicio__hour=9)
    domingo2 = reservadomingo.filter(horaInicio__hour=10)
    domingo3 = reservadomingo.filter(horaInicio__hour=11)
    domingo4 = reservadomingo.filter(horaInicio__hour=12)
    domingo5 = reservadomingo.filter(horaInicio__hour=13)
    domingo6 = reservadomingo.filter(horaInicio__hour=14)
    domingo7 = reservadomingo.filter(horaInicio__hour=15)
    domingo8 = reservadomingo.filter(horaInicio__hour=16)
    domingo9 = reservadomingo.filter(horaInicio__hour=17)
    context = {
        'count': count,
        'reservas': reservas,
        'prestamos': prestamos,
        'lunes': lunes,
        'domingo': domingo,
        'reservagrilla': reservagrilla,
        'lunes1': lunes1.first(),
        'lunes2': lunes2.first(),
        'lunes3': lunes3.first(),
        'lunes4': lunes4.first(),
        'lunes5': lunes5.first(),
        'lunes6': lunes6.first(),
        'lunes7': lunes7.first(),
        'lunes8': lunes8.first(),
        'lunes9': lunes9.first(),
        'martes1': martes1.first(),
        'martes2': martes2.first(),
        'martes3': martes3.first(),
        'martes4': martes4.first(),
        'martes5': martes5.first(),
        'martes6': martes6.first(),
        'martes7': martes7.first(),
        'martes8': martes8.first(),
        'martes9': martes9.first(),
        'miercoles1': miercoles1.first(),
        'miercoles2': miercoles2.first(),
        'miercoles3': miercoles3.first(),
        'miercoles4': miercoles4.first(),
        'miercoles5': miercoles5.first(),
        'miercoles6': miercoles6.first(),
        'miercoles7': miercoles7.first(),
        'miercoles8': miercoles8.first(),
        'miercoles9': miercoles9.first(),
        'jueves1': jueves1.first(),
        'jueves2': jueves2.first(),
        'jueves3': jueves3.first(),
        'jueves4': jueves4.first(),
        'jueves5': jueves5.first(),
        'jueves6': jueves6.first(),
        'jueves7': jueves7.first(),
        'jueves8': jueves8.first(),
        'jueves9': jueves9.first(),
        'viernes1': viernes1.first(),
        'viernes2': viernes2.first(),
        'viernes3': viernes3.first(),
        'viernes4': viernes4.first(),
        'viernes5': viernes5.first(),
        'viernes6': viernes6.first(),
        'viernes7': viernes7.first(),
        'viernes8': viernes8.first(),
        'viernes9': viernes9.first(),
        'sabado1': sabado1.first(),
        'sabado2': sabado2.first(),
        'sabado3': sabado3.first(),
        'sabado4': sabado4.first(),
        'sabado5': sabado5.first(),
        'sabado6': sabado6.first(),
        'sabado7': sabado7.first(),
        'sabado8': sabado8.first(),
        'sabado9': sabado9.first(),
        'domingo1': domingo1.first(),
        'domingo2': domingo2.first(),
        'domingo3': domingo3.first(),
        'domingo4': domingo4.first(),
        'domingo5': domingo5.first(),
        'domingo6': domingo6.first(),
        'domingo7': domingo7.first(),
        'domingo8': domingo8.first(),
        'domingo9': domingo9.first(),}
    return render(request, 'Inventario/landingPageUsuario.html', context)


def landingPageAdministrador(request):
    count = 0
    if (request.GET.get('count', '')):
        count = int(request.GET.get('count', ''))
    reservas = Reserva.objects.order_by('-fechaReserva').exclude(articulo__isnull=True).filter(estado='P')
    prestamos = Prestamo.objects.order_by('-fechaPrestamo')
    prestamosperdidos=prestamos.filter(estado='D')
    prestamospendientes=prestamos.filter(estado='P')
    prestamosrecibidos=prestamos.filter(estado='C')
    lunes = (date.today() - timedelta(date.today().isoweekday() - 1) + timedelta(7 * count))
    domingo = (date.today() + timedelta(7 - date.today().isoweekday()) + timedelta(7 * count))
    reservagrilla = Reserva.objects.filter(fechaReserva__range=[lunes, domingo]).exclude(espacio__isnull=True)
    reservalunes = reservagrilla.filter(fechaReserva__week_day=2)
    reservamartes = reservagrilla.filter(fechaReserva__week_day=3)
    reservamiercoles = reservagrilla.filter(fechaReserva__week_day=4)
    reservajueves = reservagrilla.filter(fechaReserva__week_day=5)
    reservaviernes = reservagrilla.filter(fechaReserva__week_day=6)
    reservasabado = reservagrilla.filter(fechaReserva__week_day=7)
    reservadomingo = reservagrilla.filter(fechaReserva__week_day=1)
    lunes1 = reservalunes.filter(horaInicio__hour=9)
    lunes2 = reservalunes.filter(horaInicio__hour=10)
    lunes3 = reservalunes.filter(horaInicio__hour=11)
    lunes4 = reservalunes.filter(horaInicio__hour=12)
    lunes5 = reservalunes.filter(horaInicio__hour=13)
    lunes6 = reservalunes.filter(horaInicio__hour=14)
    lunes7 = reservalunes.filter(horaInicio__hour=15)
    lunes8 = reservalunes.filter(horaInicio__hour=16)
    lunes9 = reservalunes.filter(horaInicio__hour=17)
    lunes10 = reservalunes.filter(horaInicio__hour=18)
    martes1 = reservamartes.filter(horaInicio__hour=9)
    martes2 = reservamartes.filter(horaInicio__hour=10)
    martes3 = reservamartes.filter(horaInicio__hour=11)
    martes4 = reservamartes.filter(horaInicio__hour=12)
    martes5 = reservamartes.filter(horaInicio__hour=13)
    martes6 = reservamartes.filter(horaInicio__hour=14)
    martes7 = reservamartes.filter(horaInicio__hour=15)
    martes8 = reservamartes.filter(horaInicio__hour=16)
    martes9 = reservamartes.filter(horaInicio__hour=17)
    martes10 = reservamartes.filter(horaInicio__hour=18)
    miercoles1 = reservamiercoles.filter(horaInicio__hour=9)
    miercoles2 = reservamiercoles.filter(horaInicio__hour=10)
    miercoles3 = reservamiercoles.filter(horaInicio__hour=11)
    miercoles4 = reservamiercoles.filter(horaInicio__hour=12)
    miercoles5 = reservamiercoles.filter(horaInicio__hour=13)
    miercoles6 = reservamiercoles.filter(horaInicio__hour=14)
    miercoles7 = reservamiercoles.filter(horaInicio__hour=15)
    miercoles8 = reservamiercoles.filter(horaInicio__hour=16)
    miercoles9 = reservamiercoles.filter(horaInicio__hour=17)
    miercoles10 = reservamiercoles.filter(horaInicio__hour=18)
    jueves1 = reservajueves.filter(horaInicio__hour=9)
    jueves2 = reservajueves.filter(horaInicio__hour=10)
    jueves3 = reservajueves.filter(horaInicio__hour=11)
    jueves4 = reservajueves.filter(horaInicio__hour=12)
    jueves5 = reservajueves.filter(horaInicio__hour=13)
    jueves6 = reservajueves.filter(horaInicio__hour=14)
    jueves7 = reservajueves.filter(horaInicio__hour=15)
    jueves8 = reservajueves.filter(horaInicio__hour=16)
    jueves9 = reservajueves.filter(horaInicio__hour=17)
    jueves10 = reservajueves.filter(horaInicio__hour=18)
    viernes1 = reservaviernes.filter(horaInicio__hour=9)
    viernes2 = reservaviernes.filter(horaInicio__hour=10)
    viernes3 = reservaviernes.filter(horaInicio__hour=11)
    viernes4 = reservaviernes.filter(horaInicio__hour=12)
    viernes5 = reservaviernes.filter(horaInicio__hour=13)
    viernes6 = reservaviernes.filter(horaInicio__hour=14)
    viernes7 = reservaviernes.filter(horaInicio__hour=15)
    viernes8 = reservaviernes.filter(horaInicio__hour=16)
    viernes9 = reservaviernes.filter(horaInicio__hour=17)
    viernes10 = reservaviernes.filter(horaInicio__hour=18)
    sabado1 = reservasabado.filter(horaInicio__hour=9)
    sabado2 = reservasabado.filter(horaInicio__hour=10)
    sabado3 = reservasabado.filter(horaInicio__hour=11)
    sabado4 = reservasabado.filter(horaInicio__hour=12)
    sabado5 = reservasabado.filter(horaInicio__hour=13)
    sabado6 = reservasabado.filter(horaInicio__hour=14)
    sabado7 = reservasabado.filter(horaInicio__hour=15)
    sabado8 = reservasabado.filter(horaInicio__hour=16)
    sabado9 = reservasabado.filter(horaInicio__hour=17)
    sabado10 = reservasabado.filter(horaInicio__hour=18)
    domingo1 = reservadomingo.filter(horaInicio__hour=9)
    domingo2 = reservadomingo.filter(horaInicio__hour=10)
    domingo3 = reservadomingo.filter(horaInicio__hour=11)
    domingo4 = reservadomingo.filter(horaInicio__hour=12)
    domingo5 = reservadomingo.filter(horaInicio__hour=13)
    domingo6 = reservadomingo.filter(horaInicio__hour=14)
    domingo7 = reservadomingo.filter(horaInicio__hour=15)
    domingo8 = reservadomingo.filter(horaInicio__hour=16)
    domingo9 = reservadomingo.filter(horaInicio__hour=17)
    domingo10 = reservadomingo.filter(horaInicio__hour=18)
    context = {
        'ESTADOS_RESERVA': ESTADOS_RESERVA,
        'count': count,
        'reservas': reservas,
        'prestamos': prestamos,
        'prestamospendientes': prestamospendientes,
        'prestamosperdidos': prestamosperdidos,
        'prestamosrecibidos': prestamosrecibidos,
        'lunes': lunes,
        'domingo': domingo,
        'reservagrilla': reservagrilla,
        'lunes1': lunes1.first(),
        'lunes2': lunes2.first(),
        'lunes3': lunes3.first(),
        'lunes4': lunes4.first(),
        'lunes5': lunes5.first(),
        'lunes6': lunes6.first(),
        'lunes7': lunes7.first(),
        'lunes8': lunes8.first(),
        'lunes9': lunes9.first(),
        'lunes10': lunes10.first(),
        'martes1': martes1.first(),
        'martes2': martes2.first(),
        'martes3': martes3.first(),
        'martes4': martes4.first(),
        'martes5': martes5.first(),
        'martes6': martes6.first(),
        'martes7': martes7.first(),
        'martes8': martes8.first(),
        'martes9': martes9.first(),
        'martes10': martes10.first(),
        'miercoles1': miercoles1.first(),
        'miercoles2': miercoles2.first(),
        'miercoles3': miercoles3.first(),
        'miercoles4': miercoles4.first(),
        'miercoles5': miercoles5.first(),
        'miercoles6': miercoles6.first(),
        'miercoles7': miercoles7.first(),
        'miercoles8': miercoles8.first(),
        'miercoles9': miercoles9.first(),
        'miercoles10': miercoles10.first(),
        'jueves1': jueves1.first(),
        'jueves2': jueves2.first(),
        'jueves3': jueves3.first(),
        'jueves4': jueves4.first(),
        'jueves5': jueves5.first(),
        'jueves6': jueves6.first(),
        'jueves7': jueves7.first(),
        'jueves8': jueves8.first(),
        'jueves9': jueves9.first(),
        'jueves10': jueves10.first(),
        'viernes1': viernes1.first(),
        'viernes2': viernes2.first(),
        'viernes3': viernes3.first(),
        'viernes4': viernes4.first(),
        'viernes5': viernes5.first(),
        'viernes6': viernes6.first(),
        'viernes7': viernes7.first(),
        'viernes8': viernes8.first(),
        'viernes9': viernes9.first(),
        'viernes10': viernes10.first(),
        'sabado1': sabado1.first(),
        'sabado2': sabado2.first(),
        'sabado3': sabado3.first(),
        'sabado4': sabado4.first(),
        'sabado5': sabado5.first(),
        'sabado6': sabado6.first(),
        'sabado7': sabado7.first(),
        'sabado8': sabado8.first(),
        'sabado9': sabado9.first(),
        'sabado10': sabado10.first(),
        'domingo1': domingo1.first(),
        'domingo2': domingo2.first(),
        'domingo3': domingo3.first(),
        'domingo4': domingo4.first(),
        'domingo5': domingo5.first(),
        'domingo6': domingo6.first(),
        'domingo7': domingo7.first(),
        'domingo8': domingo8.first(),
        'domingo9': domingo9.first(),
        'domingo10': domingo10.first()
    }
    return render(request, 'Inventario/landingPageAdministrador.html', context)


def perfilUsuario(request, usuarioId):
    if (not request.user.is_authenticated) or (not request.user.esAdmin and request.user.id != usuarioId):
        return redirect('Inventario:index')

    usuario = get_object_or_404(Usuario, id=usuarioId)

    reservas = Reserva.objects.filter(solicitante=usuario).order_by('-fechaCreacion')
    registro_reservas = []
    for reserva in reservas:
        registro = {}
        registro['reserva'] = reserva
        registro['estados'] = RegistroEstadoReserva.objects.filter(reserva_asociada=reserva).order_by('-fecha')
        registro_reservas.append(registro)

    prestamos = Prestamo.objects.filter(reserva__solicitante=usuario).order_by('-fechaPrestamo')
    registro_prestamos = []
    for prestamo in prestamos:
        registro = {}
        registro['prestamo'] = prestamo
        registro['estados'] = RegistroEstadoPrestamo.objects.filter(prestamo_asociado=prestamo).order_by('-fecha')
        registro_prestamos.append(registro)

    context = {
        'registro_reservas': registro_reservas,
        'registro_prestamos': registro_prestamos,
        'usuarioId': usuarioId,
        'PENDIENTE': PENDIENTE,
        'ENTREGADO': ENTREGADO,
        'RECHAZADO': RECHAZADO,
        'RECIBIDO': RECIBIDO,
        'PERDIDO': PERDIDO,
        'ESTADOS_RESERVA': ESTADOS_RESERVA,
        'ESTADOS_PRESTAMO': ESTADOS_PRESTAMO,
    }
    return render(request, 'Inventario/perfilUsuario.html', context)


def fichaArticulo(request, articuloId):
    reservas = Reserva.objects.filter(articulo__id=articuloId).order_by('-fechaCreacion')
    articulo = get_object_or_404(Articulo, id=articuloId)
    reserva_form = SimpleReservaForm(user=request.user, initial={'articulo': articulo, 'solicitante': request.user,
                                                                 'estado': PENDIENTE})

    context = {
        'reservas': reservas,
        'articulo': articulo,
        'DISPONIBLE': DISPONIBLE,
        'PRESTAMO': PRESTAMO,
        'REPARACION': REPARACION,
        'PERDIDO': PERDIDO,
        'reserva_form': reserva_form,
    }
    return render(request, 'Inventario/fichaArticulo.html', context)


def fichaReserva(request, reservaId):
    return HttpResponse('Ficha reserva ' + str(reservaId))


def fichaPrestamo(request, prestamoId):
    return HttpResponse('Ficha prestamo ' + str(prestamoId))


def fichaEspacio(request, espacioId):
    reservas = Reserva.objects.filter(espacio__id=espacioId).order_by('-fechaCreacion')
    espacio = get_object_or_404(Espacio, id=espacioId)
    reserva_form = SimpleReservaForm(user=request.user, initial={'espacio': espacio, 'solicitante': request.user,
                                                                 'estado': PENDIENTE})

    context = {
        'reservas': reservas,
        'espacio': espacio,
        'DISPONIBLE': DISPONIBLE,
        'PRESTAMO': PRESTAMO,
        'REPARACION': REPARACION,
        'reserva_form': reserva_form,
    }
    return render(request, 'Inventario/fichaEspacio.html', context)


def eliminarListaReservas(request):
    next = request.POST.get('next', reverse('Inventario:index'))
    if request.method == 'POST':
        is_valid = request.user.is_authenticated
        reservas = request.POST.getlist('reservas')
        if len(reservas) != len(set(reservas)):
            is_valid = False
        for reservaId in reservas:
            if not is_valid:
                break
            reserva = Reserva.objects.filter(id=reservaId).first()
            if reserva is None or (not request.user.esAdmin and reserva.solicitante != request.user):
                is_valid = False

        if is_valid:
            for reservaId in reservas:
                reserva = Reserva.objects.get(id=reservaId)
                reserva.delete()
            messages.success(request, 'Se eliminaron ' + str(len(reservas)) + ' reservas')
        else:
            messages.error(request, 'Hubo un error, no se eliminaron las reservas seleccionadas')

    return redirect(next)


def eliminarListaPrestamos(request):
    next = request.POST.get('next', reverse('Inventario:index'))
    if request.method == 'POST':
        is_valid = request.user.is_authenticated and request.user.esAdmin
        prestamos = request.POST.getlist('prestamos')
        if len(prestamos) != len(set(prestamos)):
            is_valid = False
        for prestamoId in prestamos:
            if not is_valid:
                break
            prestamo = Prestamo.objects.filter(id=prestamoId).first()
            if prestamo is None:
                is_valid = False

        if is_valid:
            for prestamoId in prestamos:
                prestamo = Prestamo.objects.get(id=prestamoId)
                prestamo.delete()
            messages.success(request, 'Se eliminaron ' + str(len(prestamos)) + ' préstamos')
        else:
            messages.error(request, 'Hubo un error, no se eliminaron las préstamos seleccionados')

    return redirect(next)


def cambiarEstadoListaReservas(request):
    next = request.POST.get('next', reverse('Inventario:index'))
    if request.method == 'POST':
        is_valid = request.user.is_authenticated and request.user.esAdmin and in_estados(ESTADOS_RESERVA,
                                                                                         request.POST.get('estado'))
        reservas = request.POST.getlist('reservas')
        if len(reservas) != len(set(reservas)):
            is_valid = False

        for reservaId in reservas:
            if not is_valid:
                break
            reserva = Reserva.objects.filter(id=reservaId).first()
            if reserva is None:
                is_valid = False

        if is_valid:
            for reservaId in reservas:
                reserva = Reserva.objects.get(id=reservaId)
                data = model_to_dict(reserva)
                data['estado'] = request.POST.get('estado')
                form = ReservaForm(data=data, instance=reserva, user=request.user)
                if form.is_valid():
                    form.save()
            messages.success(request, 'Se cambiaron ' + str(len(reservas)) + ' reservas')
        else:
            messages.error(request, 'Hubo un error, no se cambió el estado de las reservas seleccionadas')

    return redirect(next)


def cambiarEstadoListaPrestamos(request):
    next = request.POST.get('next', reverse('Inventario:index'))
    if request.method == 'POST':
        is_valid = request.user.is_authenticated and request.user.esAdmin and in_estados(ESTADOS_PRESTAMO,
                                                                                         request.POST.get('estado'))
        prestamos = request.POST.getlist('prestamos')
        if len(prestamos) != len(set(prestamos)):
            is_valid = False

        for prestamoId in prestamos:
            if not is_valid:
                break
            prestamo = Prestamo.objects.filter(id=prestamoId).first()
            if prestamo is None:
                is_valid = False

        if is_valid:
            for prestamoId in prestamos:
                prestamo = Prestamo.objects.get(id=prestamoId)
                data = model_to_dict(prestamo)
                data['estado'] = request.POST.get('estado')
                form = PrestamoForm(data=data, instance=prestamo, user=request.user)
                if form.is_valid():
                    form.save()
            messages.success(request, 'Se cambiaron ' + str(len(prestamos)) + ' préstamos')
        else:
            messages.error(request, 'Hubo un error, no se cambió el estado de los préstamos seleccionados')

    return redirect(next)


def password_change(request):
    if not request.user.is_authenticated:
        return redirect('Inventario:index')
    form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'La contraseña fue cambiada.')
            return redirect('Inventario:index')
        else:
            messages.error(request, 'Hubo un error en el formulario, la contraseña no fue cambiada.')

    return render(request, 'Inventario/password_change.html', {'form': form})


class UsuarioCreate(UserPassesTestMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Inventario/usuario_form.html'
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.is_authenticated and self.request.user.esAdmin:
            return reverse('Inventario:usuarioUpdate', kwargs={'pk': self.object.pk})
        return reverse('Inventario:index')

    def test_func(self):
        return not self.request.user.is_authenticated or self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el usuario no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El usuario fue creado.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class UsuarioUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'Inventario/usuario_form.html'
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:usuarioUpdate', kwargs=self.kwargs)
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el usuario no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El usuario fue modificado.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class UsuarioDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('Inventario:index')
    template_name = 'Inventario/usuario_form_confirm.html'
    redirect_field_name = None

    def test_func(self):
        return self.request.user.esAdmin

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El usuario fue eliminado.')
        return super().delete(self, request, *args, **kwargs)


class ReservaCreate(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:reservaUpdate', kwargs={'pk': self.object.pk})
        return reverse('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, la reserva no fue creada.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'La reserva fue creada.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ReservaUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:reservaUpdate', kwargs=self.kwargs)
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, la reserva no fue modificada.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'La reserva fue modificada.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ReservaDelete(LoginRequiredMixin, DeleteView):
    model = Reserva
    success_url = reverse_lazy('Inventario:index')
    redirect_field_name = None

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'La reserva fue eliminada.')
        return super().delete(self, request, *args, **kwargs)


class PrestamoCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:prestamoUpdate', kwargs={'pk': self.object.pk})
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el préstamo no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El préstamo fue creado.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PrestamoUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:prestamoUpdate', kwargs=self.kwargs)
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el préstamo no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El préstamo fue modificado.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PrestamoDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Prestamo
    success_url = reverse_lazy('Inventario:index')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.esAdmin

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El préstamo fue eliminado.')
        return super().delete(self, request, *args, **kwargs)


class ArticuloCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:articuloUpdate', kwargs={'pk': self.object.pk})
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el artículo no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El artículo fue creado.')
        return super().form_valid(form)


class ArticuloUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    form_class = ArticuloForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:articuloUpdate', kwargs=self.kwargs)
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el artículo no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El artículo fue modificado.')
        return super().form_valid(form)


class ArticuloDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    success_url = reverse_lazy('Inventario:index')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.esAdmin

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El artículo fue eliminado.')
        return super().delete(self, request, *args, **kwargs)


class EspacioCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Espacio
    form_class = EspacioForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:espacioUpdate', kwargs={'pk': self.object.pk})
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el espacio no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El espacio fue creado.')
        return super().form_valid(form)


class EspacioUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Espacio
    form_class = EspacioForm
    redirect_field_name = None

    def get_success_url(self):
        if self.request.user.esAdmin:
            return reverse('Inventario:espacioUpdate', kwargs=self.kwargs)
        return reverse('Inventario:index')

    def test_func(self):
        return self.request.user.esAdmin

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el espacio no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El espacio fue modificado.')
        return super().form_valid(form)


class EspacioDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Espacio
    success_url = reverse_lazy('Inventario:index')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.esAdmin

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El espacio fue eliminado.')
        return super().delete(self, request, *args, **kwargs)

# Create your views here.
from datetime import timedelta, date

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from Inventario.forms import UsuarioForm, ReservaForm, PrestamoForm, ArticuloForm, EspacioForm, CustomPasswordChangeForm
from Inventario.models import Reserva, Prestamo, Articulo, Espacio, Usuario, PENDIENTE, ENTREGADO, RECHAZADO, RECIBIDO, \
    PERDIDO, in_estados, ESTADOS_RESERVA, ESTADOS_PRESTAMO


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
    context = {}
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


def perfilUsuario(request, usuarioId):
    if (not request.user.is_authenticated) or (not request.user.esAdmin and request.user.id != usuarioId):
        return redirect('Inventario:index')

    try:
        usuario = Usuario.objects.get(id=usuarioId)

        reservas = Reserva.objects.filter(solicitante=usuario)
        prestamos = Prestamo.objects.filter(reserva__solicitante=usuario)

        context = {
            'reservas': reservas,
            'prestamos': prestamos,
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

    except Usuario.DoesNotExist:
        return redirect('Inventario:index')


def fichaArticulo(request, articuloId):
    reservas = Reserva.objects.order_by('-fechaReserva')
    articulo = Articulo.objects

    context = {
        'reservas': reservas,
        'articulo': articulo,
    }
    return render(request, 'Inventario/fichaArticulo.html', context)


def fichaReserva(request, reservaId):
    return HttpResponse('Ficha reserva ' + str(reservaId))


def fichaPrestamo(request, prestamoId):
    return HttpResponse('Ficha prestamo ' + str(prestamoId))


def fichaEspacio(request, espacioId):
    return HttpResponse('Ficha espacio ' + str(espacioId))


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

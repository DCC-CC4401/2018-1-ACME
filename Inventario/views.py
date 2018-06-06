# Create your views here.
from datetime import timedelta, date

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from Inventario.forms import UsuarioForm, ReservaForm, PrestamoForm, ArticuloForm, EspacioForm
from Inventario.models import Reserva, Prestamo, Articulo, Espacio, Usuario, PENDIENTE, ENTREGADO, RECHAZADO


def index(request):
    if request.user.is_authenticated:
        if request.user.esAdmin:
            return landingPageAdministrador(request)
        else:
            return landingPageUsuario(request)
    else:
        return redirect('customAuth:login')


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


def perfilUsuario(request, usuarioId):
    if (not request.user.is_authenticated) or (not request.user.esAdmin and request.user.id != usuarioId):
        return redirect('Inventario:index')

    try:
        Usuario.objects.get(id=usuarioId)
    except Usuario.DoesNotExist:
        return redirect('Inventario:index')

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
    context['PENDIENTE'] = PENDIENTE
    context['ENTREGADO'] = ENTREGADO
    context['RECHAZADO'] = RECHAZADO
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


def fichaReserva(request, reservaId):
    return HttpResponse('hola')


def fichaPrestamo(request, prestamoId):
    return None


def fichaEspacio(request, espacioId):
    return None


class UsuarioCreate(CreateView):
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy('Inventario:index')
    template_name = 'Inventario/usuario_form.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el usuario no fue creada.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El usuario fue creado.')
        return super().form_valid(form)


class UsuarioUpdate(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy('Inventario:index')
    template_name = 'Inventario/usuario_form.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el usuario no fue modificada.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El usuario fue modificado.')
        return super().form_valid(form)


class UsuarioDelete(DeleteView):
    model = Usuario
    success_url = reverse_lazy('Inventario:index')
    template_name = 'Inventario/usuario_form_confirm.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El usuario fue eliminado.')
        return super().delete(self, request, *args, **kwargs)


class ReservaCreate(CreateView):
    model = Reserva
    form_class = ReservaForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, la reserva no fue creada.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'La reserva fue creada.')
        return super().form_valid(form)


class ReservaUpdate(UpdateView):
    model = Reserva
    form_class = ReservaForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, la reserva no fue modificada.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'La reserva fue modificada.')
        return super().form_valid(form)


class ReservaDelete(DeleteView):
    model = Reserva
    success_url = reverse_lazy('Inventario:index')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'La reserva fue eliminada.')
        return super().delete(self, request, *args, **kwargs)


class PrestamoCreate(CreateView):
    model = Prestamo
    form_class = PrestamoForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el préstamo no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El préstamo fue creado.')
        return super().form_valid(form)


class PrestamoUpdate(UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el préstamo no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El préstamo fue modificado.')
        return super().form_valid(form)


class PrestamoDelete(DeleteView):
    model = Prestamo
    success_url = reverse_lazy('Inventario:index')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El préstamo fue eliminado.')
        return super().delete(self, request, *args, **kwargs)


class ArticuloCreate(CreateView):
    model = Articulo
    form_class = ArticuloForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el artículo no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El artículo fue creado.')
        return super().form_valid(form)


class ArticuloUpdate(UpdateView):
    model = Articulo
    form_class = ArticuloForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el artículo no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El artículo fue modificado.')
        return super().form_valid(form)


class ArticuloDelete(DeleteView):
    model = Articulo
    success_url = reverse_lazy('Inventario:index')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El artículo fue eliminado.')
        return super().delete(self, request, *args, **kwargs)


class EspacioCreate(CreateView):
    model = Espacio
    form_class = EspacioForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el espacio no fue creado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El espacio fue creado.')
        return super().form_valid(form)


class EspacioUpdate(UpdateView):
    model = Espacio
    form_class = EspacioForm
    success_url = reverse_lazy('Inventario:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario, el espacio no fue modificado.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'El espacio fue modificado.')
        return super().form_valid(form)


class EspacioDelete(DeleteView):
    model = Espacio
    success_url = reverse_lazy('Inventario:index')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El espacio fue eliminado.')
        return super().delete(self, request, *args, **kwargs)

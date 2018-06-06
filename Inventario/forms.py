from django.forms import ModelForm

from .models import Usuario, Reserva, Prestamo, Articulo, Espacio

registeredForms = {}


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'apellido', 'esAdmin', 'estado']
        labels = {
            'username': 'RUT',
            'email': 'Email',
        }
        help_texts = {
            'username': None,
            'password': None,
        }


class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = ['articulo', 'espacio', 'fechaReserva', 'horaInicio', 'horaTermino', 'estado']


class PrestamoForm(ModelForm):
    class Meta:
        model = Prestamo
        fields = ['articulo', 'espacio', 'fechaPrestamo', 'solicitante', 'horaInicio', 'horaTermino', 'estado']


class ArticuloForm(ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre', 'descripcion', 'foto', 'estado']


class EspacioForm(ModelForm):
    class Meta:
        model = Espacio
        fields = ['nombre', 'descripcion', 'foto', 'capacidad', 'estado']

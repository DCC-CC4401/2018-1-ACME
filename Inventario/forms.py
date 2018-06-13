import re
from datetime import datetime, timedelta, time

from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm, PasswordInput, Textarea, CharField, ValidationError, HiddenInput
from django.utils import timezone

from Inventario.widgets import SwitchWidget
from .models import Usuario, Reserva, Prestamo, Articulo, Espacio, PENDIENTE, DISPONIBLE


class UsuarioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if not self.user.is_authenticated or not self.user.esAdmin:
            self.fields['esAdmin'].widget = HiddenInput()
            self.fields['esAdmin'].required = False
            self.fields['estado'].widget = HiddenInput()
            self.fields['estado'].required = False
        if self.instance.pk is not None:
            self.fields['password'].widget = HiddenInput()
            self.fields['password'].required = False
            self.fields['password2'].widget = HiddenInput()
            self.fields['password2'].required = False

    password2 = CharField(widget=PasswordInput, label='Repita la contraseña')

    class Meta:
        model = Usuario
        fields = ['email', 'username', 'nombre', 'apellido', 'estado', 'esAdmin', 'password']
        labels = {
            'username': 'RUT',
            'password': 'Contraseña',
        }
        help_texts = {
            'email': 'e.g. ejemplo@ejemplo.com',
            'username': 'e.g. 12345678-9',
            'password': 'Mínimo 8 caracteres',
        }
        widgets = {
            'password': PasswordInput,
            'esAdmin': SwitchWidget,
        }
        error_messages = {
            'username': {
                'required': 'Porfavor ingrese un RUT',
                'invalid': 'El RUT ingresado es inválido',
                'unique': 'El RUT ingresado ya existe'
            },
            'email': {
                'required': 'Porfavor ingrese un email',
                'invalid': 'El email ingresado es inválido',
                'unique': 'El email ingresado ya existe'
            },
            'nombre': {
                'required': 'Porfavor ingrese un nombre',
                'invalid': 'El nombre ingresado es inválido',
            },
            'apellido': {
                'required': 'Porfavor ingrese un apellido',
                'invalid': 'El apellido ingresado es invalido',
            },
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[0-9]{7,8}-[0-9kK]$', username):
            raise ValidationError('El RUT ingresado es inválido')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if self.instance.pk is None and len(password) < 8:
            raise ValidationError('El largo de la contraseña debe ser mayor o igual a 8')
        if self.instance.pk is not None:
            password = self.instance.password
        return password

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if self.instance.pk is not None:
            password2 = self.instance.password
        return password2

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password is not None and password2 is not None and password != password2:
            self.add_error('password', 'Las contraseñas ingresadas no coinciden')
            self.add_error('password2', '')

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.instance.pk is None:
            user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class ReservaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if not self.user.esAdmin:
            self.fields['solicitante'].widget = HiddenInput()
            self.fields['solicitante'].required = False
            self.fields['estado'].widget = HiddenInput()
            self.fields['estado'].required = False

    class Meta:
        model = Reserva
        fields = ['articulo', 'espacio', 'solicitante', 'fechaReserva', 'horaInicio', 'horaTermino', 'estado']

        widgets = {
            'fechaReserva': DatePickerInput,
            'horaInicio': TimePickerInput,
            'horaTermino': TimePickerInput,
        }

        help_texts = {
            'fechaReserva': 'mm/dd/aaaa',
            'horaInicio': 'La hora de inicio debe ser mayor o igual a las 9:00',
            'horaTermino': 'La hora de término debe ser menor o igual a las 18:00',
        }

    def clean_solicitante(self):
        solicitante = self.cleaned_data.get('solicitante')
        if solicitante is None or not self.user.esAdmin:
            solicitante = self.user
        return solicitante

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado is None or not self.user.esAdmin:
            estado = PENDIENTE
            if self.instance.pk is not None:
                estado = self.instance.estado
        return estado

    def clean(self):
        super().clean()
        articulo = self.cleaned_data.get('articulo')
        espacio = self.cleaned_data.get('espacio')
        fechaReserva = self.cleaned_data.get('fechaReserva')
        horaInicio = self.cleaned_data.get('horaInicio')
        horaTermino = self.cleaned_data.get('horaTermino')
        print(self.cleaned_data)
        if articulo is None and espacio is None:
            self.add_error('articulo', 'Porfavor escoge un artículo o un espacio')
            self.add_error('espacio', 'Porfavor escoge un artículo o un espacio')
        if articulo is not None and espacio is not None:
            self.add_error('articulo', 'Solo puedes escoger un artículo o un espacio')
            self.add_error('espacio', 'Solo puedes escoger un artículo o un espacio')
        if self.instance.pk is None and datetime.combine(fechaReserva, horaInicio) < datetime.now() + timedelta(
                minutes=55):
            self.add_error('fechaReserva',
                           'Solo puedes reservar con 1 hora de anticipación con el inicio de fecha/hora de la reserva')
        if horaInicio > horaTermino:
            self.add_error('horaTermino', 'La hora de término debe ser mayor a la hora de inicio')
        if horaInicio < time(hour=9):
            self.add_error('horaInicio', 'La hora de inicio debe ser mayor o igual a las 9:00')
        if horaTermino > time(hour=18):
            self.add_error('horaTermino', 'La hora de término debe ser menor o igual a las 18:00')

        return self.cleaned_data

    def save(self, commit=True):
        reserva = super().save(commit=False)
        if self.instance.pk is None:
            reserva.fechaCreacion = timezone.now()
        if commit:
            reserva.save()
        return reserva


class PrestamoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Prestamo
        fields = ['reserva', 'estado']

        error_messages = {
            'reserva': {
                'required': 'Porfavor ingresa una reserva',
                'unique': 'Ya existe un préstamo asociado a esta reserva'
            }
        }

    def clean(self):
        super().clean()
        reserva = self.cleaned_data.get('reserva')
        if reserva is not None:
            articulo = reserva.articulo
            espacio = reserva.espacio
            if articulo is not None and articulo.estado != DISPONIBLE:
                self.add_error('reserva', 'El artículo no está disponible para prestar')
            if espacio is not None and espacio.estado != DISPONIBLE:
                self.add_error('reserva', 'El espacio no está disponible para prestar')
        return self.cleaned_data

    def save(self, commit=True):
        prestamo = super().save(commit=False)
        if self.instance.pk is None:
            prestamo.fechaCreacion = timezone.now()
        if commit:
            prestamo.save()
        return prestamo


class ArticuloForm(ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre', 'descripcion', 'foto', 'estado']

        widgets = {
            'descripcion': Textarea,
        }

        help_texts = {
            'foto': 'Opcional'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        return descripcion

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        return foto


class EspacioForm(ModelForm):
    class Meta:
        model = Espacio
        fields = ['nombre', 'capacidad', 'descripcion', 'foto', 'estado']

        widgets = {
            'descripcion': Textarea,
        }

        help_texts = {
            'foto': 'Opcional'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        return descripcion

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        return foto

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        return capacidad


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {'password_incorrect': 'La contraseña ingresada es incorrecta',
                      'password_mismatch': 'Las contraseñas ingresadas no coinciden'}
    old_password = CharField(
        required=True,
        label='Contraseña antigua',
        widget=PasswordInput,
        error_messages={
            'required': 'Ingrese la contraseña antigua',
        },
    )
    new_password1 = CharField(
        required=True,
        label='Nueva Contraseña',
        widget=PasswordInput,
        error_messages={
            'required': 'Ingrese la nueva contraseña',
        },
    )
    new_password2 = CharField(
        required=True,
        label='Repita la nueva Contraseña',
        widget=PasswordInput,
        error_messages={
            'required': 'Ingrese la nueva contraseña',
        },
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 8:
            raise ValidationError('El largo de la contraseña debe ser mayor o igual a 8')
        return password

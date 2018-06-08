import re

from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.forms import ModelForm, PasswordInput, Textarea, CharField, ValidationError, HiddenInput

from Inventario.widgets import SwitchWidget
from .models import Usuario, Reserva, Prestamo, Articulo, Espacio


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
            'horaInicio': 'hh:mm',
            'horaTermino': 'hh:mm',
        }

    def clean_articulo(self):
        articulo = self.cleaned_data.get('articulo')
        return articulo

    def clean_espacio(self):
        espacio = self.cleaned_data.get('espacio')
        return espacio

    def clean_fechaReserva(self):
        fechaReserva = self.cleaned_data.get('fechaReserva')
        return fechaReserva

    def clean_horaInicio(self):
        horaInicio = self.cleaned_data.get('horaInicio')
        return horaInicio

    def clean_horaTermino(self):
        horaTermino = self.cleaned_data.get('horaTermino')
        return horaTermino

    def clean_solicitante(self):
        solicitante = self.cleaned_data.get('solicitante')
        if solicitante is None:
            solicitante = self.user
        return solicitante


class PrestamoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Prestamo
        fields = ['articulo', 'espacio', 'fechaPrestamo', 'solicitante', 'horaInicio', 'horaTermino', 'estado']

        widgets = {
            'fechaPrestamo': DatePickerInput,
            'horaInicio': TimePickerInput,
            'horaTermino': TimePickerInput,
        }

        help_texts = {
            'fechaPrestamo': 'mm/dd/aaaa',
            'horaInicio': 'hh:mm',
            'horaTermino': 'hh:mm',
        }

    def clean_articulo(self):
        articulo = self.cleaned_data.get('articulo')
        return articulo

    def clean_espacio(self):
        espacio = self.cleaned_data.get('espacio')
        return espacio

    def clean_fechaPrestamo(self):
        fechaPrestamo = self.cleaned_data.get('fechaPrestamo')
        return fechaPrestamo

    def clean_solicitante(self):
        solicitante = self.cleaned_data.get('solicitante')
        return solicitante

    def clean_horaInicio(self):
        horaInicio = self.cleaned_data.get('horaInicio')
        return horaInicio

    def clean_horaTermino(self):
        horaTermino = self.cleaned_data.get('horaTermino')
        return horaTermino


class ArticuloForm(ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre', 'descripcion', 'foto', 'estado']

        widgets = {
            'descripcion': Textarea,
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

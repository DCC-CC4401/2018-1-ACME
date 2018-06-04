from django import forms
from django.forms import ModelForm

from .models import Reserva, EstadoReserva


class ReservaForm(ModelForm):
    estado = forms.ChoiceField(choices=EstadoReserva.ESTADO_CHOICES)

    class Meta:
        model = Reserva
        fields = ('articulo', 'espacio', 'fechaReserva', 'horaInicio', 'horaTermino')
        labels = {
            'articulo': 'Artículo',
            'espacio': 'Espacio',
            'fechaReserva': 'Fecha de la Reserva',
            'horaInicio': 'Hora de Inicio',
            'horaTermino': 'Hora de Término',
        }

    def save(self, commit=True):
        reserva = super(ReservaForm, self).save(commit=False)
        reserva.ultimoEstado = EstadoReserva.objects.create(estado=self.estado, reserva_asociada=reserva)
        if commit:
            reserva.save()
        return reserva

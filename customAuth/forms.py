from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class RegistrationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'esAdmin')
        labels = {
            'username': 'RUT',
            'email': 'Email',
            'password': 'Contraseña',
            'esAdmin': 'Administrador',
        }
        help_texts = {
            'username': None,
            'password': None,
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

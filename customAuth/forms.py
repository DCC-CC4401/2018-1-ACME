from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
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


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the label for the "username" field.
        self.fields['username'].label = 'RUT o Email'
        self.fields['password'].label = 'Contraseña'


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

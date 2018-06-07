from django.contrib.auth import views as auth_views
from django.urls import path

from Inventario import views
from customAuth.forms import LoginForm

app_name = 'customAuth'

urlpatterns = [
    path('login/', auth_views.login, {'authentication_form': LoginForm}, name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('registrar/', views.UsuarioCreate.as_view(), name='registrar'),
]

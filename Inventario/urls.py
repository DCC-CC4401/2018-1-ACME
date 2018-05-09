from django.urls import path

from . import views

app_name = 'Inventario'

urlpatterns = [
    path('', views.index, name='index'),
    path('usuario/<int:userId>/', views.perfilUsuario, name='perfilUsuario'),
    path('registrar', views.registrar, name='registrar'),
    path('lpadministrador/', views.landingPageAdministrador, name='lpa'),
    path('articulo/<int:articuloId>/', views.fichaArticulo, name='fichaArticulo')
]

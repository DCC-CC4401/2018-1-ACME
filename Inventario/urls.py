from django.urls import path

from . import views

app_name = 'Inventario'

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfilUsuario, name='perfilUsuario'),
    path('articulo/<int:articuloId>/', views.fichaArticulo, name='fichaArticulo')
]

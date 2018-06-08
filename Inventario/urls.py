from django.urls import path

from . import views

app_name = 'Inventario'

urlpatterns = [
    path('', views.index, name='index'),

    path('usuario/<int:usuarioId>/', views.perfilUsuario, name='perfilUsuario'),
    path('usuario/crear/', views.UsuarioCreate.as_view(), name='usuarioCreate'),
    path('usuario/<int:pk>/editar/', views.UsuarioUpdate.as_view(), name='usuarioUpdate'),
    path('usuario/<int:pk>/eliminar/', views.UsuarioDelete.as_view(), name='usuarioDelete'),
    path('usuario/cambiar-contraseña/', views.password_change, name='passwordChange'),

    path('reserva/<int:reservaId>/', views.fichaReserva, name='fichaReserva'),
    path('reserva/crear/', views.ReservaCreate.as_view(), name='reservaCreate'),
    path('reserva/<int:pk>/editar/', views.ReservaUpdate.as_view(), name='reservaUpdate'),
    path('reserva/<int:pk>/eliminar/', views.ReservaDelete.as_view(), name='reservaDelete'),

    path('prestamo/<int:prestamoId>/', views.fichaPrestamo, name='fichaPrestamo'),
    path('prestamo/crear/', views.PrestamoCreate.as_view(), name='prestamoCreate'),
    path('prestamo/<int:pk>/editar/', views.PrestamoUpdate.as_view(), name='prestamoUpdate'),
    path('prestamo/<int:pk>/eliminar/', views.PrestamoDelete.as_view(), name='prestamoDelete'),

    path('articulo/<int:articuloId>/', views.fichaArticulo, name='fichaArticulo'),
    path('articulo/crear/', views.ArticuloCreate.as_view(), name='articuloCreate'),
    path('articulo/<int:pk>/editar/', views.ArticuloUpdate.as_view(), name='articuloUpdate'),
    path('articulo/<int:pk>/eliminar/', views.ArticuloDelete.as_view(), name='articuloDelete'),

    path('espacio/<int:espacioId>/', views.fichaEspacio, name='fichaEspacio'),
    path('espacio/crear/', views.EspacioCreate.as_view(), name='espacioCreate'),
    path('espacio/<int:pk>/editar/', views.EspacioUpdate.as_view(), name='espacioUpdate'),
    path('espacio/<int:pk>/eliminar/', views.EspacioDelete.as_view(), name='espacioDelete'),

    path('lpadmin/', views.landingPageAdministrador, name='lpAdmin'),
    path('lpusuario/', views.landingPageUsuario, name='lpUsuario'),
    path('buscar/', views.busquedaArticulos, name='buscar'),
    path('buscar/articulo/<int:articuloId>/', views.fichaArticulo, name='articuloEncontrado')
]

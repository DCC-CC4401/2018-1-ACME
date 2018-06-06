from django.urls import path

from . import views

app_name = 'Inventario'

urlpatterns = [
    path('', views.index, name='index'),

    path('usuario/<int:usuarioId>/', views.perfilUsuario, name='perfilUsuario'),
    path('usuario/create/', views.UsuarioCreate.as_view(), name='usuarioCreate'),
    path('usuario/<int:pk>/update/', views.UsuarioUpdate.as_view(), name='usuarioUpdate'),
    path('usuario/<int:pk>/delete/', views.UsuarioDelete.as_view(), name='usuarioDelete'),

    path('reserva/<int:reservaId>/', views.fichaReserva, name='fichaReserva'),
    path('reserva/create/', views.ReservaCreate.as_view(), name='reservaCreate'),
    path('reserva/<int:pk>/update/', views.ReservaUpdate.as_view(), name='reservaUpdate'),
    path('reserva/<int:pk>/delete/', views.ReservaDelete.as_view(), name='reservaDelete'),

    path('prestamo/<int:prestamoId>/', views.fichaPrestamo, name='fichaPrestamo'),
    path('prestamo/create/', views.PrestamoCreate.as_view(), name='prestamoCreate'),
    path('prestamo/<int:pk>/update/', views.PrestamoUpdate.as_view(), name='prestamoUpdate'),
    path('prestamo/<int:pk>/delete/', views.PrestamoDelete.as_view(), name='prestamoDelete'),

    path('articulo/<int:articuloId>/', views.fichaArticulo, name='fichaArticulo'),
    path('articulo/create/', views.ArticuloCreate.as_view(), name='articuloCreate'),
    path('articulo/<int:pk>/update/', views.ArticuloUpdate.as_view(), name='articuloUpdate'),
    path('articulo/<int:pk>/delete/', views.ArticuloDelete.as_view(), name='articuloDelete'),

    path('espacio/<int:espacioId>/', views.fichaEspacio, name='fichaEspacio'),
    path('espacio/create/', views.EspacioCreate.as_view(), name='espacioCreate'),
    path('espacio/<int:pk>/update/', views.EspacioUpdate.as_view(), name='espacioUpdate'),
    path('espacio/<int:pk>/delete/', views.EspacioDelete.as_view(), name='espacioDelete'),

    path('lpadmin/', views.landingPageAdministrador, name='lpAdmin'),
    path('lpusuario/', views.landingPageUsuario, name='lpUsuario')
]

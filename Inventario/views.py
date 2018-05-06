# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello World")


def landingPageUsuario(request):
    context = {}
    return render(request, 'Inventario/landingPageUsuario.html', context)


def landingPageAdministrador(request):
    context = {}
    return render(request, 'Inventario/landingPageAdministrador.html', context)


def paginaRegistro(request):
    context = {}
    return render(request, 'Inventario/registro.html', context)


def perfilUsuario(request, userId):
    context = {}
    return render(request, 'Inventario/perfilUsuario.html', context)


def iniciarSesion(request):
    pass

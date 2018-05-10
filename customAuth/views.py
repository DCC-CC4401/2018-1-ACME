from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from customAuth.forms import RegistrationForm


def registrar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Inventario:index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Inventario:index'))
    form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
from django.shortcuts import reverse, render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import ArchivoCrudo, InsumoQGeoidal
from .forms import ArchivoCrudoForm, InsumoQGeoidalForm
import os


class subirArchivosCrudosVista(CreateView):
    """Vista para almacenar archivos crudos o devolver la vista no exitosa

    Args:
        CreateView: clase de vista para crear objetos en el modelo

    Returns:
        HTML: devolver página html de subida exitosa o insatisfactoria
    """
    model           = ArchivoCrudo
    form_class      = ArchivoCrudoForm
    template_name   = 'entrada_datos/subir_archivo_crudo.html'

    def post(self, request, *args, **kwargs):
        form = ArchivoCrudoForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            object.usuario = User.objects.get(id=1)
            object.save()
            return HttpResponseRedirect(reverse('inicio'))
        else:
            return render(request,
                          'entrada_datos/subir_archivo_crudo.html',
                          {'form': form})
        
class subirInsumosVista(CreateView):
    """Vista para almacenar archivos crudos o devolver la vista no exitosa

    Args:
        CreateView: clase de vista para crear objetos en el modelo

    Returns:
        HTML: devolver página html de subida exitosa o insatisfactoria
    """
    model           = InsumoQGeoidal
    form_class      = InsumoQGeoidalForm
    template_name   = 'entrada_datos/subir_insumo.html'

    def post(self, request, *args, **kwargs):
        form = InsumoQGeoidalForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            object.usuario = User.objects.get(id=1)
            object.save()
            return HttpResponseRedirect(reverse('inicio'))
        else:
            return render(request,
                          'entrada_datos/subir_insumo.html',
                          {'form': form})
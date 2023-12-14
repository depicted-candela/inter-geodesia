
from django.shortcuts import render, reverse
from django.core import serializers
from django.core.files import File
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, View
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
from qgeoidcol.read import Lector
from qgeoidcol.alturas import Alturas
from qgeoidcol.gravedades import Gravedades
from qgeoidcol.derivas import Derivas
from entrada_datos.models import ArchivoCrudo
from estandarizar.models import Correcciones
from .models import ProyectoAereo, Proyectos, DatoAereo, Linea
from .forms import ProyectoAereoForm
from typing import Any
from io import BytesIO
import shutil
import os


class VistaListaCrudos(TemplateView):

    template_name = 'estandarizar/lista_crudos.html'

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tipo    = request.GET.get('tipo')
            form    = self.get_form_based_on_tipo(tipo)
            html    = render_to_string('estandarizar/parametros.html',
                                       {'form': form,
                                        'tipo': tipo},
                                       request=request)
            return JsonResponse({'parametros': html})
        context     = {'l_crudos': ArchivoCrudo.objects.all()}
        return self.render_to_response(context)

    def get_form_based_on_tipo(self, tipo):
        # Replace this logic with your actual form selection logic
        if tipo == 'aerogravimetria':
            return ProyectoAereoForm()
        else:
            return None  # or a default form
    
    def post(self, request, *args, **kwargs):
        s_item_id   = request.POST.get('selected_item')
        archivo_cr  = get_object_or_404(ArchivoCrudo, id=s_item_id)
        proyectos   = Proyectos()
        proyectos.save()
        proyectos   = Proyectos.objects.first()
        form        = ProyectoAereoForm(request.POST, request.FILES)
        vars        = request.POST
        files       = request.FILES
        object      = form.save(commit=False)
        object.usuario= archivo_cr.usuario
        object.pry_id= proyectos
        arch_orig_p = archivo_cr.archivo.path
        arch_dest_n = os.path.basename(arch_orig_p)
        arch_dest_p = os.path.join(settings.BASE_DIR,
                                   'media/estandarizados/gravimetria',
                                   arch_dest_n)
        if not os.path.exists(os.path.dirname(arch_dest_p)): os.makedirs(os.path.dirname(arch_dest_p))
        shutil.copy2(arch_orig_p, arch_dest_p)
        with open(arch_dest_p, 'rb') as file_content:
            object.archivo = File(file_content, name=arch_dest_n)
            object.save()
        if archivo_cr.tipo == 'aerogravimetria':
            self._aerogravimetria_puntual(arch_dest_p, vars=vars, files=files)
            return render(request, 'estandarizar/lista_crudos.html', {'message':'Proyecto subido'})

    def _detecta_correccion_por_deriva_aerogravimetria(self, proyecto, **kwargs):
        lector  = Lector()
        deriva  = lector.leer(BytesIO(kwargs['files']['deriva'].read()),
                              metodo='deriva',
                              empresa=kwargs['vars']['org'],
                              concatenador=BytesIO(kwargs['files']['concatenador'].read()),
                              delimitador=' ')
        derivas = Derivas()
        return derivas.corregir_deriva(proyecto, deriva)

    def _aerogravimetria_puntual(self, path_file, **kwargs):
        lector  = Lector()
        archivo = lector.leer(path_file,
                              metodo='proyecto_gravedad',
                              tipo='crudo-aereo',
                              longitud=kwargs['vars']['longitud'],
                              latitud=kwargs['vars']['latitud'])
        if 'deriva' in kwargs['files'].keys() and 'concatenador' in kwargs['files'].keys():
            lines = self._detecta_correccion_por_deriva_aerogravimetria(archivo, **kwargs)
        else: lines = None
        gravedad= Gravedades()
        gravedad.calcular_gravedad(archivo,
                                   'carson_indirect',
                                   free_air=kwargs['vars']['anomalia_aire_libre'],
                                   free_air_corr=kwargs['vars']['correcion_aire_libre'])
        alturas = Alturas()
        alturas.calcular_altura(archivo,
                                'altura_anomala',
                                modelo='eigen-6c4')
        alturas.calcular_altura(archivo,
                                'ondulacion_geoidal',
                                modelo='eigen-6c4')
        adf     = archivo.df
        data_vars = {
            'fid'   : adf[kwargs['vars']['original_id']],
            'geom'  : adf['GEOM'],
            'grav_h'  : adf['GRAV'],
            'h_adj' : adf[kwargs['vars']['alt_h_a']],
            'h_cru' : adf[kwargs['vars']['alt_h_c']],
            'radar' : adf[kwargs['vars']['radar']],
            'linea' : adf[kwargs['vars']['linea']],
            'zeta'  : adf['zeta'],
            'N'     : adf['N'],
            'drift_l': lines,
            'fecha' : kwargs['vars']['fecha'],
        }
        self._crea_aerogravimetria_puntual(data_vars=data_vars)

    def _crea_aerogravimetria_puntual(self, **kwargs):
        proyecto= Proyectos.objects.first()
        paereo  = ProyectoAereo.objects.first()
        tot     = len(kwargs['data_vars']['fid'])
        lineas  = set()
        for i, id in enumerate(kwargs['data_vars']['fid']):
            linea_      = kwargs['data_vars']['linea'][i]
            if type(linea_) != str:
                linea_  = str(linea_)
            if linea_ not in lineas:
                lineas.add(linea_)
                linea__ = Linea(name=linea_, pry_id=proyecto)
                linea__.save()
                self.determina_derivas(linea_, kwargs['data_vars']['drift_l'])
            dato_aereo  = DatoAereo(
                h_cru=kwargs['data_vars']['h_cru'].loc[i],
                h_adj=kwargs['data_vars']['h_adj'].loc[i],
                grav_h=kwargs['data_vars']['grav_h'].loc[i],
                radar=kwargs['data_vars']['radar'].loc[i],
                linea=linea__,
                or_id=id,
                geom=Point(kwargs['data_vars']['geom'].loc[i].x,
                           kwargs['data_vars']['geom'].loc[i].y),
                zeta=kwargs['data_vars']['zeta'].loc[i],
                N=kwargs['data_vars']['N'].loc[i],
                pry=paereo,
                fecha=kwargs['data_vars']['fecha']
            )
            percent     = (i / tot)
            print(f'\r{percent*100:.2f}% de puntos arriba', end='\r')
            dato_aereo.save()
    
    def determina_derivas(self, linea, d_linea):
        if d_linea and float(linea) in d_linea:
            correccion  = Correcciones(
                linea=Linea.objects.first(),
                deriva=True,
                marea=None)
            correccion.save()


class ProcessSelectedItemsView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the list of selected item IDs from the form
        selected_items = request.POST.getlist('selected_items')

        # Retrieve the action selected by the user
        action = request.POST.get('action')

        if action:
            # Fetch the selected items from the database
            items_to_process = ArchivoCrudo.objects.filter(id__in=selected_items)

            if action == 'action1':
                # Perform Action 1 on the selected items
                for item in items_to_process:
                    # Action 1 logic here
                    pass
            elif action == 'action2':
                # Perform Action 2 on the selected items
                for item in items_to_process:
                    # Action 2 logic here
                    pass
            # ... handle other actions

            messages.success(request, "Selected items have been processed.")
        else:
            messages.error(request, "No action selected.")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
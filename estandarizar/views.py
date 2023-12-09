
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
from typing import Any
from entrada_datos.models import ArchivoCrudo
from .models import ProyectoAereo, Proyectos, DatoAereo, Linea
from .forms import ProyectoAereoForm
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
            self.crea_aerogravimetria_puntual(arch_dest_p,
                                         anomalia_aire_libre=vars['anomalia_aire_libre'],
                                         correcion_aire_libre=vars['correcion_aire_libre'],
                                         longitud=vars['longitud'],
                                         latitud=vars['latitud'],
                                         original_id=vars['original_id'],
                                         alt_h_a=vars['alt_h_a'],
                                         alt_h_c=vars['alt_h_c'],
                                         radar=vars['radar'],
                                         fecha=vars['fecha'],
                                         linea=vars['linea'])
            return render(request, 'estandarizar/lista_crudos.html', {'message':'Proyecto subido'})

    def crea_aerogravimetria_puntual(self, path_file, **kwargs):

        from qgeoidcol.read import Lector
        from qgeoidcol.gravedades import Gravedades

        lector  = Lector()
        archivo = lector.leer(path_file, metodo='proyecto_gravedad', tipo='crudo-aereo',
                                    longitud=kwargs['longitud'],
                                    latitud=kwargs['latitud'])
        gravedad= Gravedades()
        gravedad.calcular_gravedad(archivo, 'carson_indirect',
                                    free_air=kwargs['anomalia_aire_libre'],
                                    free_air_corr=kwargs['correcion_aire_libre'])
        proyecto= Proyectos.objects.first()
        paereo  = ProyectoAereo.objects.first()
        df      = archivo.df
        fid     = df[kwargs['original_id']]
        geom    = df['GEOM']
        grav    = df['GRAV']
        h_adj   = df[kwargs['alt_h_a']]
        h_cru   = df[kwargs['alt_h_c']]
        radar   = df[kwargs['radar']]
        linea   = df[kwargs['linea']]
        lineas  = set()
        for i, id in enumerate(fid):
            linea_   = linea[i]
            if type(linea_) != str:
                linea_ = str(linea_)
            if linea_ not in lineas:
                lineas.add(linea_)
                linea__ = Linea(name=linea_,pry_id=proyecto)
                linea__.save()
            dato_aereo = DatoAereo(
                h_cru=h_cru[i],  # Replace with actual data
                h_adj=h_adj[i],  # Replace with actual data
                grav_h=grav[i],  # Replace with actual data
                radar=radar[i],  # Replace with actual data
                linea=linea__,
                or_id=id,  # Replace with actual data
                geom=Point(geom[i].x, geom[i].y),  # Replace with actual coordinates
                xi=-999.99999,  # Replace with actual data
                pry=paereo,
                fecha=kwargs['fecha']
            )
            dato_aereo.save()


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
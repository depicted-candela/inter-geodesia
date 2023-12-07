from typing import Any
from django.shortcuts import render
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, View
from django.template.loader import render_to_string
from entrada_datos.models import ArchivoCrudo
from .forms import ProyectoAereoForm


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

        parameters = request.POST


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
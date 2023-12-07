from django.urls import path

from .views import *


urlpatterns = [
    path('listar_archivos_crudos/', VistaListaCrudos.as_view(), name='listar_archivos_crudos'),
    path('process-selected/', ProcessSelectedItemsView.as_view(), name='process_selected_items'),
]
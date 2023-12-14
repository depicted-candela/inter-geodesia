from django.urls import path

from . import views


urlpatterns = [
    path("subir_archivos_crudos", views.subirArchivosCrudosVista.as_view(), name="subir_archivos_crudos"),
    path("subir_insumos", views.subirInsumosVista.as_view(), name="subir_insumos"),
]

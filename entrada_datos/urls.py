from django.urls import path

from . import views


urlpatterns = [
    path("subir_archivos_crudos", views.subirarchivoscrudosVista.as_view(), name="subir_archivos_crudos"),
]

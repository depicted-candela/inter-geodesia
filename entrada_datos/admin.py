from django.contrib import admin
from .models import ArchivoCrudo


class ArchivoCrudoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'archivo', 'tipo', 'detalle', 'usuario')

admin.site.register(ArchivoCrudo, ArchivoCrudoAdmin)
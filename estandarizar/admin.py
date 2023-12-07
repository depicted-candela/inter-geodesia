from django.contrib import admin

from . import models as m

class ProyectosAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(m.Proyectos, ProyectosAdmin)

class LineaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'pry_id')
admin.site.register(m.Linea, LineaAdmin)

class CorreccionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'linea', 'deriva', 'marea')
admin.site.register(m.Correcciones, CorreccionesAdmin)

class ProyectoAereoAdmin(admin.ModelAdmin):
    list_display = ['id', 'exact', 'archivo', 'nombre', 'reporte', 'detalle', 'pry_id', 'org']
admin.site.register(m.ProyectoAereo, ProyectoAereoAdmin)

class ProyectoTerrestreAdmin(admin.ModelAdmin):
    list_display = ('id', 'exact', 'archivo', 'nombre', 'reporte', 'detalle', 'pry_id', 'org')
admin.site.register(m.ProyectoTerrestre, ProyectoTerrestreAdmin)

class ProyectoOceanicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exact', 'archivo', 'nombre', 'reporte', 'detalle', 'pry_id', 'org')
admin.site.register(m.ProyectoOceanico, ProyectoOceanicoAdmin)

class NivelacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cota', 'h_t', 'obsv')
admin.site.register(m.Nivelacion, NivelacionAdmin)

class GravimetriaTAdmin(admin.ModelAdmin):
    list_display = ('id', 'grav', 'h_t', 'obsv', 'tipo')
admin.site.register(m.GravimetriaT, GravimetriaTAdmin)

class DatoTerrestreAdmin(admin.ModelAdmin):
    list_display = ('id', 'nivl', 'grav', 'or_id', 'linea', 'pry')
admin.site.register(m.DatoTerrestre, DatoTerrestreAdmin)

class DatoAereoAdmin(admin.ModelAdmin):
    list_display = ('id', 'h_cru', 'h_adj', 'grav_h', 'a_a_li', 'radar', 'linea', 'or_id', 'geom', 'pry')
admin.site.register(m.DatoAereo, DatoAereoAdmin)

class DatoOceanicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pry')
admin.site.register(m.DatoOceanico, DatoOceanicoAdmin)
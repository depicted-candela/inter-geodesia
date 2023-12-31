from django import forms
from .models import ProyectoAereo


class ProyectoAereoForm(forms.ModelForm):
    
    class Meta:
        model   = ProyectoAereo
        fields = ['exact', 'nombre', 'reporte', 'detalle', 'org', 'fuente', 'elip', 'cc']
        labels  = {
            'exact': 'Exactitud (mGals)',
            'nombre': 'Nombre del proyecto',
            'reporte': 'Archivo reporte técnico del proyecto',
            'detalle': 'Observaciones del proyecto dadas por quien lo revisó',
            'org': 'Organización que levantó las observaciones del proyecto',
            'fuente': 'Fuente que compartió los datos',
            'elip': 'Elipsoide de referencia para los datos',
            'cc': 'Cross-Coupling conocido',
        }
    
    ## Inicializador de instancia SubirArchivosForm
    def __init__(self, *args, **kwargs):    
        
        ## Utilizar 
        super(ProyectoAereoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['rows'] = 8
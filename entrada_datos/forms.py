from django.forms import ModelForm
from .models import ArchivoCrudo

class ArchivoCrudoForm(ModelForm):

    """
    Formato para subir archivos de cualquier formato
    """

    class Meta:
        model   = ArchivoCrudo
        fields  = ['nombre', 'archivo', 'meta', 'tipo', 'detalle', 'fuente', 'elip']
        labels  = {
            'nombre': 'Nombre (utilice minúsculas y no tildes)',
            'archivo': 'Archivo',
            'meta': 'Reporte original con detalles',
            'tipo': 'Tipo de proyecto',
            'detalle': 'Detalles',
            'fuente': 'Fuente',
            'elip': 'Elipsoide',
        }
    
    ## Inicializador de instancia SubirArchivosForm
    def __init__(self, *args, **kwargs):    
        
        ## Utilizar 
        super(ArchivoCrudoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['rows'] = 8
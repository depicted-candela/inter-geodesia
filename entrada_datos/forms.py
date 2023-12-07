from django.forms import ModelForm
from .models import ArchivoCrudo

class ArchivoCrudoForm(ModelForm):

    """
    Formato para subir archivos de cualquier formato
    """

    class Meta:
        model   = ArchivoCrudo
        fields  = ['nombre', 'archivo', 'tipo', 'detalle']
        labels  = {
            'nombre': 'Nombre (utilice minúsculas y no tildes)',
            'archivo': 'Archivo',
            'tipo': 'Tipo de proyecto',
            'detalle': 'Detalles'
        }
    
    ## Inicializador de instancia SubirArchivosForm
    def __init__(self, *args, **kwargs):    
        
        ## Utilizar 
        super(ArchivoCrudoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['rows'] = 8
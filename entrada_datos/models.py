from django.contrib.auth.models import User
from django.db import models


class ArchivoCrudo(models.Model):
    
    """
    Clase para modelar datos crudos
    """

    OPCIONES = [
        ('aerogravimetria', 'Gravimetría aérea'),
        ('batimetria', 'Gravimetría oceánica'),
        ('nivelacion', 'Nivelación'),
        ('gravterrabs', 'Gravedad terrestre absoluta'),
        ('gravterrrel', 'Gravedad terrestre relativa'),
    ]

    ELLIP   = [
        ('7019', 'GRS80'),
        ('4326', 'WGS84'),
    ]

    FUENTES = [
        ('desc', 'Desconocido'),
        ('bgi', 'Bureau Gravimetrique International'),
        ('ecopetrol', 'Ecopetrol'),
        ('sgc', 'Servicio Geológico Colombiano')
    ]
    
    ## Variables necesarias para entender el archivo
    id      = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50, null=False)
    archivo = models.FileField(upload_to="media/crudos/datos", null=False)
    meta    = models.FileField(upload_to="media/crudos/metadatos", null=True, blank=True)
    tipo    = models.CharField(max_length=20, choices=OPCIONES, null=False)
    detalle = models.CharField(max_length=500, null=False)
    fuente  = models.CharField(max_length=20,
                               default='desc',
                               null=False,
                               choices=FUENTES)
    elip    = models.CharField(max_length=20,
                               choices=ELLIP,
                               default='7019',
                               null=False,
                               help_text="Elipsoide de las coordenadas")
    usuario = models.ForeignKey(
        User,
        related_name='archivo_crudo',
        on_delete=models.PROTECT
    )

    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'archivo crudo'
        verbose_name_plural = 'archivos crudos'

    ## Guardar el archivo temporal
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    ## Definición para la función print
    def __str__(self):
        return f"Archivo {self.nombre} de tipo {self.tipo}, proveniente del archivo {self.archivo}"


class Insumo(models.Model):
    
    """
    Clase para modelar insumos crudos
    """

    ELLIP   = [
        ('7019', 'GRS80'),
        ('4326', 'WGS84'),
    ]

    FUENTES = [
        ('icgem', 'ICGEM')
    ]
    
    ## Variables necesarias para entender el archivo
    id      = models.AutoField(primary_key=True)
    nombre  = models.CharField(max_length=50, null=False)
    detalle = models.CharField(max_length=500, null=False)
    fuente  = models.CharField(max_length=20,
                               default='desc',
                               null=False,
                               choices=FUENTES)
    elip    = models.CharField(max_length=20,
                               choices=ELLIP,
                               default='7019',
                               null=False,
                               help_text="Elipsoide de las coordenadas")
    usuario = models.ForeignKey(
        User,
        related_name='insumo',
        on_delete=models.PROTECT
    )

    class Meta:
        ## Ordenar por
        abstract            = True
        ordering            = ('-id',)

    ## Guardar el archivo temporal
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    ## Definición para la función print
    def __str__(self):
        return f"Insumo {self.nombre} proveniente del archivo {self.archivo}"

class InsumoQGeoidal(Insumo):

    MODELO = [
        ('eigen-6c4', 'EIGEN6C4'),
    ]

    VARS = [
        ('ondulacion-geoidal', 'Ondulación geoidal'),
        ('altura-anomala-superficial', 'Altura anómala superficial'),
    ]
    
    id      = models.AutoField(primary_key=True)
    modelo  = models.CharField(max_length=40, choices=MODELO, null=False)
    variable= models.CharField(max_length=40, choices=VARS, null=False)
    archivo = models.FileField(upload_to="insumos/modelos_geoidales/datos", null=False)
    meta    = models.FileField(upload_to="insumos/modelos_geoidales/metadatos", null=False)

    class Meta:

        verbose_name        = 'archivo crudo'
        verbose_name_plural = 'archivos crudos'
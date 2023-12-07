from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User


class Proyectos(models.Model):
    """Clase agregadora de todos los proyectos para el modelo geoidal
    para modelarlos en la base de datos relacional generada

    Args:
        models (models.Model): modelos de bases de datos ofrecidos por django

    Returns:
        _type_: _description_
    """
    id      = models.AutoField(primary_key=True, help_text="Identificador del proyecto")
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    ## Guardar el archivo temporal
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    ## Definición para la función print
    def __str__(self):
        return f"Proyecto {self.tipo}"


class Linea(models.Model):
    
    id      = models.AutoField(primary_key=True, help_text="Identificador de la línea")
    name    = models.CharField(max_length=30, null=False)
    pry_id  = models.ForeignKey(Proyectos, models.CASCADE, null=False)
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Línea'
        verbose_name_plural = 'Líneas'

    ## Guardar el archivo temporal
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    ## Definición para la función print
    def __str__(self):
        return f"Línea {self.name} del proyecto {self.pry_id}"


class Correcciones(models.Model):

    id      = models.AutoField(primary_key=True, help_text="Identificador de la correción para la línea")
    linea   = models.ForeignKey(Linea, models.CASCADE, null=False, help_text="Línea relacionada")
    deriva  = models.BooleanField(help_text="Si la línea tiene corrección por deriva")
    marea   = models.BooleanField(help_text="Si la línea tiene corrección por marea")


class Proyecto(models.Model):
    
    OPCIONES = [
        ('7019', 'GRS80'),
        ('4326', 'WGS84'),
    ]
    
    FUENTES = [
        ('desc', 'Desconocido'),
        ('bgi', 'Bureau Gravimetrique International'),
        ('ecopetrol', 'Ecopetrol'),
        ('sgc', 'Servicio Geológico Colombiano')
    ]
    
    id      = models.AutoField(primary_key=True, help_text="Identificador del punto")
    exact   = models.DecimalField(max_digits=4, decimal_places=3, help_text="Exactitud del proyecto")
    nombre  = models.CharField(max_length=100, null=False, help_text="Nombre del proyecto")
    detalle = models.TextField(null=False, help_text="Observaciones proveídas por quien sube el proyecto a la base de datos")
    pry_id  = models.ForeignKey(Proyectos, models.CASCADE, null=False, help_text="Proyecto general relacionado")
    fuente  = models.CharField(max_length=20,
                               default='desc',
                               null=False,
                               choices=FUENTES)
    elip    = models.CharField(max_length=20,
                               choices=OPCIONES,
                               default='7019',
                               null=False,
                               help_text="Elipsoide de las coordenadas")
    usuario = models.ForeignKey(
        User,
        related_name='proyecto_estandarizado',
        on_delete=models.PROTECT
    )

    ## Guardar el archivo temporal
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    

class ProyectoTerrestre(Proyecto):

    ORGS    = [
        ('d', 'Desconocido'),
    ]

    org     = models.CharField(choices=ORGS,
                               max_length=30,
                               null=False,
                               help_text="Organización encargada del proyecto")
    archivo = models.FileField(upload_to="archivos/gravimetria",
                            null=False,
                            help_text="Archivo del que provienen los datos")
    reporte = models.FileField(upload_to="reportes/gravimetria",
                               null=False,
                               help_text="Reporte que explica los datos")

    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Proyecto terrestre'
        verbose_name_plural = 'Proyectos terrestres'
        
    ## Definición para la función print
    def __str__(self):
        return f"Proyecto terrestre con nombre {self.nombre}"


class ProyectoOceanico(Proyecto):

    ORGS    = [
        ('d', 'Desconocido'),
    ]

    org     = models.CharField(choices=ORGS,
                               max_length=30,
                            null=False,
                            help_text="Organización encargada del proyecto")
    archivo = models.FileField(upload_to="archivos/batigravimetria",
                        null=False,
                        help_text="Archivo del que provienen los datos")
    reporte = models.FileField(upload_to="reportes/batigravimetria",
                            null=False,
                            help_text="Reporte que explica los datos")
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Proyecto oceánico'
        verbose_name_plural = 'Proyectos oceánicos'
        
    ## Definición para la función print
    def __str__(self):
        return f"Proyecto oceánico con nombre {self.nombre}"


class ProyectoAereo(Proyecto):
        
    ORGS    = [
        ('carson-h', 'Carson Hellicoperts'),
    ]
    org     = models.CharField(choices=ORGS,
                               max_length=30,
                               null=False,
                               help_text="Organización encargada del proyecto")
    archivo = models.FileField(upload_to="archivos/aerogravimetria",
                        null=False,
                        help_text="Archivo del que provienen los datos")
    reporte = models.FileField(upload_to="reportes/aerogravimetria",
                            null=False,
                            help_text="Reporte que explica los datos")
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Proyecto aéreo'
        verbose_name_plural = 'Proyectos aéreos'
        
    ## Definición para la función print
    def __str__(self):
        return f"Proyecto aéreo con nombre {self.nombre}"


class Nivelacion(models.Model):
    
    TIPO = [
        ('in-situ', 'Medida en campo'),
        ('calculada_global', 'Calculada con modelo geoidal global y SRTM'),
    ]
    
    id      = models.BigAutoField(primary_key=True, help_text="Identificador del punto")
    t_cota  = models.CharField(max_length=20,
                               default='desc',
                               choices=TIPO,
                               help_text="Tipo de medición para altura sobre el nivel del mar")
    cota    = models.DecimalField(max_digits=7,
                                  decimal_places=3,
                                  help_text="Altura sobre el nivel del mar")
    h_t     = models.DecimalField(max_digits=7,
                                  decimal_places=3,
                                  help_text="Altura geométrica h del punto")
    geom    = models.PointField(null=False, help_text="Geometría del punto")
    xi      = models.DecimalField(max_digits=15,
                                  decimal_places=12,
                                  default=-999.99,
                                  help_text="Altura anómala según modelo geoidal global")
    N       = models.DecimalField(max_digits=15,
                                  decimal_places=12,
                                  default=-999.99,
                                  help_text="Ondulación geoidal según modelo geoidal global")
    obsv    = models.CharField(max_length=200,
                               help_text="Observaciones del punto")
    fecha   = models.DateField(null=True)
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Nivelación'
        verbose_name_plural = 'Nivelaciones'
        
    ## Definición para la función print
    def __str__(self):
        return f"Nivelación #{self.id}"


class GravimetriaT(models.Model):
    
    OPCIONES = [
        ('relativa', 'Relativa'),
        ('absoluta', 'Absoluta'),
    ]
    
    id      = models.BigAutoField(primary_key=True, help_text="Identificador del punto")
    grav    = models.DecimalField(max_digits=9,
                                  decimal_places=3,
                                  null=False,
                                  help_text="Gravedad en terreno del punto")
    h_t     = models.DecimalField(max_digits=7,
                                  decimal_places=3,
                                  help_text="Altura geométrica h del punto")
    geom    = models.PointField(null=False,
                                default=Point(0.0, 0.0),
                                help_text="Geometría del punto")
    xi      = models.DecimalField(max_digits=15,
                                  decimal_places=12,
                                  default=-999.99,
                                  help_text="Altura anómala según modelo geoidal global")
    N       = models.DecimalField(max_digits=15,
                                  decimal_places=12,
                                  default=-999.99,
                                  help_text="Ondulación geoidal según modelo geoidal global")
    obsv    = models.CharField(max_length=200,
                               help_text="Observaciones del punto")
    tipo    = models.CharField(max_length=20,
                               choices=OPCIONES,
                               null=False,
                               help_text="El tipo de medición, ya sea absoluta o relativa")
    
    fecha   = models.DateField(null=True)
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Gravimetría'
        verbose_name_plural = 'Gravimetrías'
        
    ## Definición para la función print
    def __str__(self):
        return f"Gravimetría #{self.id}"
    

class DatoTerrestre(models.Model):
    
    id      = models.BigAutoField(primary_key=True, help_text="Identificador del punto")
    nivl    = models.ForeignKey(Nivelacion,
                                models.CASCADE,
                                help_text="Nivelación geodésica del punto")
    grav    = models.ForeignKey(GravimetriaT,
                                models.CASCADE,
                                help_text="Gravimetría del punto")
    or_id   = models.CharField(max_length=30,
                               null=False,
                               help_text="Nomenclatura original del punto físico")
    linea   = models.ForeignKey(Linea,
                                models.CASCADE,
                                null=False,
                                help_text="Línea asociada al punto")
    pry     = models.ForeignKey(ProyectoTerrestre,
                                models.CASCADE,
                                null=False,
                                help_text="Proyecto terrestre asociado")
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Dato gravimétrico terrestre'
        verbose_name_plural = 'Datos gravimétricos terrestres'
        
    ## Definición para la función print
    def __str__(self):
        return f"Dato gravimétrico {self.id} del proyecto {self.pry} en la línea {self.linea}"


class DatoAereo(models.Model):
    
    id      = models.BigAutoField(primary_key=True, help_text="Identificador del punto")
    h_cru   = models.DecimalField(max_digits=7,
                                  decimal_places=3,
                                  null=False,
                                  help_text="altitud geométrica cruda del avión (h)")
    h_adj   = models.DecimalField(max_digits=7,
                                  decimal_places=3,
                                  null=False,
                                  help_text="altitud geométrica ajustada del avión (h)")
    grav_h  = models.DecimalField(max_digits=9,
                                  decimal_places=3,
                                  null=False,
                                  help_text="gravedad observada en altitud geométrica del avión (h)")
    a_a_li  = models.DecimalField(max_digits=6,
                                  decimal_places=2,
                                  help_text="Anomalía de aire libre")
    radar   = models.DecimalField(max_digits=9,
                                  decimal_places=3,
                                  help_text="Altimetría de radar")
    linea   = models.ForeignKey(Linea,
                                models.CASCADE,
                                null=False,
                                help_text="Línea de vuelo relacionada al punto")
    or_id   = models.IntegerField(help_text="Identificador de punto original del vuelo")
    geom    = models.PointField(null=False, help_text="Geometría del punto")
    xi      = models.DecimalField(max_digits=15,
                                  decimal_places=12,
                                  default=-999.99999,
                                  null=False,
                                  help_text="Altura anómala según modelo geoidal global")
    pry     = models.ForeignKey(ProyectoAereo,
                                models.CASCADE,
                                null=False,
                                help_text="Proyecto aéreo asociado")
    fecha   = models.DateField(null=True)
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Dato aero-gravimétrico'
        verbose_name_plural = 'Datos aero-gravimétricos'
        
    ## Definición para la función print
    def __str__(self):
        return f"Dato aero-gravimétrico {self.id} del proyecto {self.pry} en la línea {self.linea}"


class DatoOceanico(models.Model):
    
    id      = models.BigAutoField(primary_key=True, help_text="Identificador del punto")
    geom    = models.PointField(null=False, help_text="Geometría del punto")
    pry     = models.ForeignKey(ProyectoOceanico,
                                models.CASCADE,
                                null=False,
                                help_text="Proyecto oceánico asociado")
    fecha   = models.DateField(null=True)
    
    class Meta:
        ## Ordenar por
        ordering            = ('-id',)
        verbose_name        = 'Dato bati-gravimétrico'
        verbose_name_plural = 'Datos bati-gravimétricos'
        
    ## Definición para la función print
    def __str__(self):
        return f"Dato aero-gravimétrico {self.id} del proyecto {self.pry}"
    
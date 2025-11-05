from django.db import models

class Almacen(models.Model):
    TIPO_ALMACEN_CHOICES = (
        ('material', 'Material'),
        ('archivos', 'Archivos')
    )
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    )
    nro_almacen = models.SmallIntegerField(blank=False, null=False)
    tipo_almacen = models.CharField(
        max_length=8, blank=False,
        null=False, choices=TIPO_ALMACEN_CHOICES
    )
    ubicacion = models.TextField()
    estado_almacen = models.CharField(
        max_length=8, blank=False,
        null=False, choices=ESTADO_CHOICES,
        default='activo'
    )
    
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Almacén'
        verbose_name_plural = 'Almacenes'
        constraints = [
            models.UniqueConstraint(
                fields=['nro_almacen', 'tipo_almacen'],
                name='unique_nro_almacen_tipo_almacen'
            )
        ]
        
    def __str__(self):
        return f"Almacen {self.nro_almacen} de {self.tipo_almacen}"

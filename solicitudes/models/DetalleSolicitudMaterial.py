from django.db import models
from materiales.models.Material import Material
from .SolicitudMaterial import SolicitudMaterial

class DetalleSolicitudMaterial(models.Model):
    ESTADO_ENTREGA_SOLICITUD = (
        ('reservado', 'reservado'),
        ('entregado', 'entregado')
    )
    cantidad_solicitada = models.PositiveSmallIntegerField(default=1, blank=False, null=False)
    estado_detalle = models.CharField(
        max_length=9, blank=False, null=False,
        choices=ESTADO_ENTREGA_SOLICITUD, default='reservado'
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(SolicitudMaterial, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Detalle de Solicitud de Material"
        verbose_name_plural = "Detalles de Solicitud de Material"
        constraints = [
            models.UniqueConstraint(
                fields=['material', 'solicitud'],
                name='unique_material_solicitud'
            )
        ]
    
    def __str__(self):
        return f"Solicitud: {self.solicitud.codigo_solicitud} - Material {self.material.descripcion}"

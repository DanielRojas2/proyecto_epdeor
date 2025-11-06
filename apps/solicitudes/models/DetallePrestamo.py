from django.db import models
from .PrestamoTomo import PrestamoTomo
from ...inventarios.models.AsignacionTomo import AsignacionTomo

class DetallePrestamo(models.Model):
    ESTADO_DETALLE_TOMO_PRESTAMO = (
        ('pendiente', 'Pendiente'),
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto')
    )
    estado_detalle_tomo = models.CharField(
        max_length=9, blank=False,
        null=False, default='pendiente',
        choices=ESTADO_DETALLE_TOMO_PRESTAMO
    )
    tomo_solicitado = models.ForeignKey(AsignacionTomo, on_delete=models.CASCADE)
    codigo_prestamo = models.ForeignKey(PrestamoTomo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Detalle de Préstamo'
        verbose_name_plural = 'Detalles de Préstamo'
        constraints = [
            models.UniqueConstraint(
                fields=['tomo_solicitado', 'codigo_prestamo'],
                name='unique_tomo_solicitado_codigo_prestamo'
            )
        ]
    
    def __str__(self):
        return f"Solicitud {self.codigo_prestamo.codigo_prestamo}, Tomo Solicitado {self.tomo_solicitado.tomo.titulo}. Estado de la Solicitud {self.estado_detalle_tomo}"

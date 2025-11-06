from django.db import models
from ...inventarios.models.AsignacionTomo import AsignacionTomo
from .PrestamoTomo import PrestamoTomo

class DetallePrestamo(models.Model):
    ESTADO_TOMO = (
        ('pendiente', 'Pendiente'),
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
        ('dañado', 'Dañado'),
    )

    tomo = models.ForeignKey(AsignacionTomo, on_delete=models.CASCADE)
    prestamo = models.ForeignKey(PrestamoTomo, on_delete=models.CASCADE, related_name='detalles')
    estado_tomo_prestamo = models.CharField(max_length=10, choices=ESTADO_TOMO, default='pendiente')
    fecha_prestamo = models.DateField(blank=True, null=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Detalle de Préstamo'
        verbose_name_plural = 'Detalles de Préstamo'
        constraints = [
            models.UniqueConstraint(
                fields=['tomo', 'prestamo'],
                name='unique_tomo_prestamo'
            )
        ]

    def __str__(self):
        return f"Tomo {self.tomo.tomo.nro_tomo} - {self.get_estado_tomo_prestamo_display()}"

    def marcar_como_devuelto(self):
        """Marca este tomo como devuelto y actualiza su estado en AsignacionTomo."""
        from datetime import date
        self.estado_tomo_prestamo = 'devuelto'
        self.fecha_devolucion = date.today()
        self.save()

        asignacion = self.tomo
        asignacion.estado_tomo = 'disponible'
        asignacion.save()

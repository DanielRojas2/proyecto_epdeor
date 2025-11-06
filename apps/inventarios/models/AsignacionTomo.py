from django.db import models
from ...almacenes.models.NivelEstante import NivelEstante
from ...archivos.models.Tomo import Tomo

class AsignacionTomo(models.Model):
    ESTADO_TOMO_CHOICES = (
        ('prestado', 'Prestado'),
        ('disponible', 'Disponible'),
    )
    fecha_asignacion = models.DateField(auto_now_add=True)
    hora_asigancion = models.TimeField(auto_now_add=True)
    estado_tomo = models.CharField(max_length=10, blank=False, null=False, default='disponible')
    espacio_ocupado = models.SmallIntegerField(default=5, blank=False, null=False)
    estante_almacen = models.ForeignKey(NivelEstante, on_delete=models.CASCADE)
    tomo = models.ForeignKey(Tomo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Asignación de Tomo'
        verbose_name_plural = 'Asignaciones de Tomos'
        constraints = [
            models.UniqueConstraint(
                fields=['estante_almacen', 'tomo'],
                name='unique_estante_almacen_tomo',
            )
        ]

    def __str__(self):
        return f"Tomo Asignado {self.tomo.titulo}, Estante {self.estante_almacen.estante.nro_estante}, Nivel {self.estante_almacen.nivel.nro_nivel}"

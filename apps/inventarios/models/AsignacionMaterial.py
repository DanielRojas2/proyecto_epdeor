from django.db import models
from ...almacenes.models.NivelEstante import NivelEstante
from ...materiales.models.Material import Material

class AsignacionMaterial(models.Model):
    fecha_asignacion = models.DateField(auto_now_add=True)
    hora_asigancion = models.TimeField(auto_now_add=True)
    cantidad_asignacion = models.SmallIntegerField(default=1, blank=False, null=False)
    espacio_ocupado = models.SmallIntegerField(default=5, blank=False, null=False)
    estante_almacen = models.ForeignKey(NivelEstante, on_delete=models.CASCADE)
    material_asignado = models.ForeignKey(Material, on_delete=models.CASCADE)
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
        return f"Material Asignado {self.material.descripcion}, Estante {self.estante_almacen.estante.nro_estante}, Nivel {self.estante_almacen.nivel.nro_nivel}"

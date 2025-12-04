# solicitudes/models/EntregaMaterialSolicitado.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EntregaMaterialSolicitado(models.Model):
    cantidad_entregada = models.PositiveIntegerField()
    solicitud = models.ForeignKey('SolicitudMaterial', on_delete=models.CASCADE)
    material_entregado = models.ForeignKey('materiales.Material', on_delete=models.CASCADE)
    entregado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entregas_realizadas')
    fecha_entrega = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Entrega de Material Solicitado'
        verbose_name_plural = 'Entregas de Materiales Solicitados'
        ordering = ['-fecha_entrega']

    def __str__(self):
        return f"Entrega {self.id} - {self.cantidad_entregada} unidades"

    def save(self, *args, **kwargs):
        if not self.fecha_entrega:
            self.fecha_entrega = timezone.now()
        super().save(*args, **kwargs)

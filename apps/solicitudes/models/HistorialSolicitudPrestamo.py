from django.db import models
from django.contrib.auth.models import User
from .SolicitudPrestamo import SolicitudPrestamo

class HistorialSolicitudPrestamo(models.Model):
    solicitud = models.ForeignKey(
        SolicitudPrestamo,
        on_delete=models.CASCADE,
        related_name='historial'
    )
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.CharField(max_length=10, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=10, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Historial de Solicitud de Préstamo'
        verbose_name_plural = 'Historial de Solicitudes de Préstamo'

    def __str__(self):
        return f"Solicitud {self.solicitud.id}: {self.estado_anterior} → {self.estado_nuevo}"

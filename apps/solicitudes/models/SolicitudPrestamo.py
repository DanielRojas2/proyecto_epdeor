from django.db import models
from django.contrib.auth.models import User
from .PrestamoTomo import PrestamoTomo

class SolicitudPrestamo(models.Model):
    ROL_ACCION = (
        ('prestante', 'Prestante'),
        ('solicitante', 'Solicitante')
    )
    ESTADO_SOLICITUD = (
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado')
    )
    rol_solicitud = models.CharField(
        max_length=11, blank=False, null=False, default='solicitante', choices=ROL_ACCION
    )
    estado_solicitud = models.CharField(
        max_length=9, blank=False, null=False, default='pendiente', choices=ESTADO_SOLICITUD
    )
    observacion = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    prestamo = models.ForeignKey(PrestamoTomo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Solicitud de Préstamo'
        verbose_name_plural = 'Solicitudes de Préstamo'
        
    def __str__(self):
        return f"{self.usuario} - {self.prestamo}"
    

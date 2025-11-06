from django.db import models
from django.contrib.auth.models import User
from .PrestamoTomo import PrestamoTomo

class SolicitudPrestamo(models.Model):
    ESTADO_SOLICITUD = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada')
    )
    ROL_SOLICITUD = (
        ('solicitante', 'Solicitante'),
        ('prestante', 'Prestante')
    )
    estado_solicitud = models.CharField(
        max_length=9, blank=False,
        null=False, default='pendiente',
        choices=ESTADO_SOLICITUD
    )
    rol_solicitud = models.CharField(
        max_length=11, blank=False,
        null=False, default='solicitante',
        choices=ROL_SOLICITUD
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_prestamo = models.ForeignKey(PrestamoTomo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Solicitud de Préstamo'
        verbose_name_plural = 'Solicitudes de Préstamos'
    
    def __str__(self):
        return f"Solicitante {self.usuario.username}, Solicitud {self.codigo_prestamo.codigo_prestamo}. Estado Solicitud {self.estado_solicitud}"

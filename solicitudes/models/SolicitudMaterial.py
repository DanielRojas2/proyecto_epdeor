from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SolicitudMaterial(models.Model):
    ESTADO_SOLICITUD = (
        ('pendiente', 'pendiente'),
        ('aprobada', 'aprobada'),
        ('rechazada', 'rechazada'),
        ('finalizada', 'finalizada'),
    )

    codigo_solicitud = models.CharField(max_length=5, unique=True)
    fecha_solicitud = models.DateField(auto_now_add=True)
    hora_solicitud = models.TimeField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=10, choices=ESTADO_SOLICITUD, default='pendiente')
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    dirigido_a = models.ForeignKey(
        'personal.Personal',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="solicitudes_recibidas"
    )
    observación = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Solicitud de Material'
        verbose_name_plural = 'Solicitud de Materiales'

    def save(self, *args, **kwargs):
        if not self.fecha_solicitud:
            self.fecha_solicitud = timezone.localdate()
        if not self.hora_solicitud:
            self.hora_solicitud = timezone.localtime().time()

        if not self.codigo_solicitud:
            last = SolicitudMaterial.objects.order_by('-codigo_solicitud').first()
            if last and last.codigo_solicitud and last.codigo_solicitud.isdigit():
                num = int(last.codigo_solicitud) + 1
            else:
                num = 1
            self.codigo_solicitud = f"{num:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solicitud {self.codigo_solicitud} - {self.estado_solicitud}"

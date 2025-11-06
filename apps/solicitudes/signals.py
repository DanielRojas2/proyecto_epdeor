from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import SolicitudPrestamo, DetallePrestamo

@receiver(post_save, sender=SolicitudPrestamo)
def aprobar_solicitud_y_actualizar(sender, instance, **kwargs):
    if instance.estado_solicitud == 'aprobada':
        prestamo = instance.codigo_prestamo

        if not prestamo.fecha_prestamo or not prestamo.hora_prestamo:
            ahora = timezone.localtime()
            prestamo.fecha_prestamo = ahora.date()
            prestamo.hora_prestamo = ahora.time()
            prestamo.save()

        DetallePrestamo.objects.filter(codigo_prestamo=prestamo).update(
            estado_detalle_tomo='prestado'
        )

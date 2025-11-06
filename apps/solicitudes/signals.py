from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import date, datetime
from .models.SolicitudPrestamo import SolicitudPrestamo
from .models.PrestamoTomo import PrestamoTomo
from .models.DetallePrestamo import DetallePrestamo
from .models.HistorialSolicitudPrestamo import HistorialSolicitudPrestamo
from ..inventarios.models import AsignacionTomo

@receiver(post_save, sender=SolicitudPrestamo)
def crear_prestamo_si_no_existe(sender, instance, created, **kwargs):
    """
    Si se crea una solicitud y aún no tiene préstamo, se genera uno automáticamente.
    """
    if created and not instance.prestamo:
        prestamo = PrestamoTomo.objects.create(
            fecha_prestamo=date.today(),
            hora_prestamo=datetime.now().time()
        )
        instance.prestamo = prestamo
        instance.save(update_fields=['prestamo'])

@receiver(pre_save, sender=SolicitudPrestamo)
def registrar_historial_cambio_estado(sender, instance, **kwargs):
    """
    Antes de guardar una solicitud, si el estado cambió,
    se guarda un registro en el historial.
    """
    if not instance.pk:
        return

    anterior = SolicitudPrestamo.objects.get(pk=instance.pk)
    if anterior.estado_solicitud != instance.estado_solicitud:
        HistorialSolicitudPrestamo.objects.create(
            solicitud=instance,
            usuario=instance.usuario,
            estado_anterior=anterior.estado_solicitud,
            estado_nuevo=instance.estado_solicitud,
            observacion=instance.observacion,
        )

@receiver(post_save, sender=SolicitudPrestamo)
def sincronizar_estado_tomos(sender, instance, **kwargs):
    """
    Cuando una solicitud cambia de estado, se ajustan los DetallePrestamo y AsignacionTomo relacionados.
    """
    if not instance.prestamo:
        return

    detalles = DetallePrestamo.objects.filter(prestamo=instance.prestamo)

    if instance.estado_solicitud == 'aceptado':
        for detalle in detalles:
            detalle.estado_tomo_prestamo = 'prestado'
            detalle.fecha_prestamo = date.today()
            detalle.save(update_fields=['estado_tomo_prestamo', 'fecha_prestamo'])

            tomo = detalle.tomo
            tomo.estado_tomo = 'prestado'
            tomo.save(update_fields=['estado_tomo'])

    elif instance.estado_solicitud == 'rechazado':
        for detalle in detalles:
            detalle.estado_tomo_prestamo = 'pendiente'
            detalle.save(update_fields=['estado_tomo_prestamo'])

            tomo = detalle.tomo
            tomo.estado_tomo = 'disponible'
            tomo.save(update_fields=['estado_tomo'])

    elif instance.estado_solicitud == 'finalizado':
        for detalle in detalles:
            detalle.estado_tomo_prestamo = 'devuelto'
            detalle.fecha_devolucion = date.today()
            detalle.save(update_fields=['estado_tomo_prestamo', 'fecha_devolucion'])

            tomo = detalle.tomo
            tomo.estado_tomo = 'disponible'
            tomo.save(update_fields=['estado_tomo'])

@receiver(post_save, sender=DetallePrestamo)
def actualizar_tomo_individual(sender, instance, **kwargs):
    """
    Si un DetallePrestamo cambia a 'devuelto',
    el tomo físico se marca como disponible automáticamente.
    """
    if instance.estado_tomo_prestamo == 'devuelto':
        tomo = instance.tomo
        if tomo.estado_tomo != 'disponible':
            tomo.estado_tomo = 'disponible'
            tomo.save(update_fields=['estado_tomo'])

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models.Tomo import Tomo
from .models.DetalleTomo import DetalleTomo

@receiver([post_save, post_delete], sender=DetalleTomo)
def actualizar_fojas_totales(sender, instance, **kwargs):
    tomo = instance.tomo
    total_fojas = (
        DetalleTomo.objects.filter(tomo=tomo)
        .aggregate(total=models.Sum('nro_fojas'))
        .get('total') or 0
    )
    tomo.nro_fojas_total = total_fojas
    tomo.save(update_fields=['nro_fojas_total'])

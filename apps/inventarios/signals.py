from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models.AsignacionTomo import AsignacionTomo
from .models.AsignacionMaterial import AsignacionMaterial
from ..materiales.models.Material import Material
from ..almacenes.models.NivelEstante import NivelEstante

@receiver(post_save, sender=AsignacionTomo)
def actualizar_espacio_disponible_creacion_actualizacion(sender, instance, created, **kwargs):
    nivel_estante = instance.estante_almacen

    if created:
        nivel_estante.espacio_disponible -= instance.espacio_ocupado
        nivel_estante.save()
    else:
        try:
            old_instance = AsignacionTomo.objects.get(pk=instance.pk)
        except AsignacionTomo.DoesNotExist:
            old_instance = None
        
        if old_instance:
            diferencia = old_instance.espacio_ocupado - instance.espacio_ocupado
            nivel_estante.espacio_disponible += diferencia
            nivel_estante.save()

@receiver(post_delete, sender=AsignacionTomo)
def actualizar_espacio_disponible_eliminacion(sender, instance, **kwargs):
    nivel_estante = instance.estante_almacen
    nivel_estante.espacio_disponible += instance.espacio_ocupado
    nivel_estante.save()
    
@receiver(post_save, sender=AsignacionMaterial)
def actualizar_espacio_disponible_material_creacion_actualizacion(sender, instance, created, **kwargs):
    nivel_estante = instance.estante_almacen

    if created:
        nivel_estante.espacio_disponible -= instance.espacio_ocupado
        nivel_estante.save()
    else:
        try:
            old_instance = AsignacionMaterial.objects.get(pk=instance.pk)
        except AsignacionMaterial.DoesNotExist:
            old_instance = None

        if old_instance:
            diferencia = old_instance.espacio_ocupado - instance.espacio_ocupado
            nivel_estante.espacio_disponible += diferencia
            nivel_estante.save()

@receiver(post_delete, sender=AsignacionMaterial)
def actualizar_espacio_disponible_material_eliminacion(sender, instance, **kwargs):
    nivel_estante = instance.estante_almacen
    nivel_estante.espacio_disponible += instance.espacio_ocupado
    nivel_estante.save()
    
@receiver([post_save, post_delete], sender=AsignacionMaterial)
def actualizar_cantidad_existente(sender, instance, **kwargs):
    material = instance.material_asignado
    
    total_asignado = AsignacionMaterial.objects.filter(
        material_asignado=material
    ).aggregate(total=models.Sum('cantidad_asignacion'))['total'] or 0

    material.cantidad_existente = total_asignado
    material.save(update_fields=['cantidad_existente'])

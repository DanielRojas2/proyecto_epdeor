from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date
from .models.Personal import Personal
from .models.Departamento import Departamento

GERENCIA_GENERAL = "Gerencia General"

@receiver(pre_save, sender=Personal)
def pre_guardar_personal(sender, instance, **kwargs):
    hoy = date.today()
    siguiente_anio = hoy.year + 1

    if instance._state.adding:
        if not instance.baja:
            instance.baja = date(siguiente_anio, 1, 10)
    else:
        if instance.baja and instance.baja <= hoy:
            instance.estado = 'inactivo'

@receiver(post_save, sender=Personal)
def crear_o_actualizar_usuario(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        username = f"{instance.nombre.lower()}{instance.apellido_paterno.lower()}{instance.ci[:2]}"
        password = (
            f"{instance.nombre[0].upper()}"
            f"{instance.apellido_paterno[0].upper()}"
            f"{(instance.apellido_materno[0].upper() if instance.apellido_materno else '')}"
            f"{instance.ci}"
        )

        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=instance.nombre,
            last_name=f"{instance.apellido_paterno} {instance.apellido_materno or ''}".strip(),
        )

        user.is_active = (instance.estado == 'activo')
        user.save()

        instance.usuario = user
        instance.save(update_fields=['usuario'])

    else:
        if instance.usuario:
            user = instance.usuario
            user.is_active = (instance.estado == 'activo')
            user.save()

@receiver(post_save, sender=Personal)
def asignar_jefe_departamento(sender, instance, created, **kwargs):
    roles = list(instance.cargo.rol.values_list("rol", flat=True))

    if "jefe gerencia" in roles:
        try:
            dpt_gerencia = Departamento.objects.get(departamento="Gerencia General")
            if dpt_gerencia.jefe != instance:
                dpt_gerencia.jefe = instance
                dpt_gerencia.save()
        except Departamento.DoesNotExist:
            pass
        return

    if "jefe jdaf" in roles:
        try:
            dpt_jdaf = Departamento.objects.get(departamento="Jefatura Departamento de Administración y Finanzas")
            if dpt_jdaf.jefe != instance:
                dpt_jdaf.jefe = instance
                dpt_jdaf.save()
        except Departamento.DoesNotExist:
            pass
        return

    if "jefe jdoht" in roles:
        try:
            dpt_jdoht = Departamento.objects.get(departamento="Jefatura Departamento de Operaciones Hotel")
            if dpt_jdoht.jefe != instance:
                dpt_jdoht.jefe = instance
                dpt_jdoht.save()
        except Departamento.DoesNotExist:
            pass
        return

    if "jefe jdotbo" in roles:
        try:
            dpt_jdotbo = Departamento.objects.get(departamento="Jefatura Departamento de Operaciones Terminal de Buses Oruro")
            if dpt_jdotbo.jefe != instance:
                dpt_jdotbo.jefe = instance
                dpt_jdotbo.save()
        except Departamento.DoesNotExist:
            pass
        return

from django.db import models
from django.contrib.auth.models import User
from .Cargo import Cargo

class Personal(models.Model):
    ESTADO_PERSONAL = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    )
    nombre = models.CharField(max_length=25, blank=False, null=False)
    apellido_paterno = models.CharField(
        max_length=25, blank=False, null=False
    )
    apellido_materno = models.CharField(
        max_length=25, blank=True, null=True
    )
    ci = models.CharField(max_length=7, blank=False, null=False, unique=True)
    alta = models.DateField(auto_now_add=True)
    baja = models.DateField(blank=True, null=True)
    cargo = models.ForeignKey(
        Cargo, on_delete=models.CASCADE, related_name='personal',
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.CharField(
        max_length=8, blank=False,
        null=False, choices=ESTADO_PERSONAL,
        default='activo'
    )
    
    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personal"
        ordering = ['nombre', 'apellido_paterno']
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'apellido_paterno', 'apellido_materno', 'ci'],
                name='unique_nombre_apellidos_ci'
            )
        ]

    def __str__(self):
        return f"Personal: {self.nombre} {self.apellido_paterno} C.I: {self.ci}"

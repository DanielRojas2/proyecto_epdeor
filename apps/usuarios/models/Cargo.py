from django.db import models
from .Departamento import Departamento
from .Unidad import Unidad
from .Rol import Rol

class Cargo(models.Model):
    cargo = models.CharField(
        max_length=100, unique=True,
        blank=False, null=False
    )
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE,
        related_name='cargos_departamento',
        blank=False, null=False
    )
    unidad = models.ForeignKey(
        Unidad, on_delete=models.CASCADE,
        related_name='cargos_unidad',
        blank=False, null=False
    )
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='cargos_rol')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['creado']
        constraints = [
            models.UniqueConstraint(
                fields=['cargo', 'departamento', 'unidad'],
                name='unique_cargo_departamento_unidad'
            )
        ]

    def __str__(self):
        return self.cargo

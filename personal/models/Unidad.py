from django.db import models

class Unidad(models.Model):
    unidad = models.CharField(
        max_length=100, unique=True,
        blank=False, null=False
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        ordering = ['creado']

    def __str__(self):
        return self.unidad

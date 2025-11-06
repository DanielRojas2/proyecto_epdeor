from django.db import models

class UdM(models.Model):
    unidad_de_medida = models.CharField(
        max_length=20, blank=False, null=False, unique=True
    )
    presentacion = models.CharField(
        max_length=35, blank=False, null=False
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return f"UdM: {self.unidad_de_medida} - Presentación: {self.presentacion}"

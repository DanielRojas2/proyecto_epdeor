from django.db import models

class Almacen(models.Model):
    nro_almacen = models.PositiveSmallIntegerField(blank=False, null=False)
    descripcion = models.CharField(max_length=100, blank=False, null=False)
    ubicacion = models.TextField(blank=False, null=False)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Almacén'
        verbose_name_plural = 'Almacenes'

    def __str__(self):
        return f"Almacén {self.nro_almacen} - {self.descripcion}. Ubicación: {self.ubicacion}"

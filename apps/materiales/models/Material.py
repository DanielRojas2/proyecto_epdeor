from django.db import models
from .PartidaPresupuestaria import PartidaPresupuestaria
from .UdM import UdM

class Material(models.Model):
    descripcion = models.CharField(
        max_length=100, blank=False, null=False, unique=True
    )
    nivel_minimo = models.PositiveIntegerField(
        default=5, blank=False, null=False
    )
    cantidad_existente = models.PositiveIntegerField(blank=True, null=True)
    partida = models.ForeignKey(
        PartidaPresupuestaria, on_delete=models.CASCADE
    )
    udm = models.ForeignKey(UdM, on_delete=models.CASCADE)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"{self.descripcion} - {self.partida.partida}: {self.cantidad_existente}"

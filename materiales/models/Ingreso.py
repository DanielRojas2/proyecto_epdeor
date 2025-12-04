from django.db import models
from .Proveedor import Proveedor

class Ingreso(models.Model):
    nro_ingreso = models.CharField(max_length=10, blank=False, null=False, unique=True)
    fecha_ingreso = models.DateField(blank=False, null=False)
    factura = models.CharField(max_length=10, blank=False, null=False)
    h_ruta = models.CharField(max_length=25, blank=False, null=False)
    orden_compra = models.CharField(max_length=15, blank=False, null=False)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    almacen = models.ForeignKey('Almacen', on_delete=models.CASCADE)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'

    def __str__(self):
        return f"Nro Ingreso: {self.nro_ingreso} - Fecha: {self.fecha_ingreso}"

from django.db import models

class Proveedor(models.Model):
    proveedor = models.CharField(max_length=100, blank=False, null=False)
    nit = models.CharField(max_length=12, blank=False, null=False)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        constraints = [
            models.UniqueConstraint(
                fields=['proveedor', 'nit'],
                name='unique_proveedor_nit'
            )
        ]

    def __str__(self):
        return f"Proveedor: {self.proveedor} - NIT: {self.nit}"

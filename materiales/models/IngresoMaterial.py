from django.db import models
from .Material import Material
from .Ingreso import Ingreso

class IngresoMaterial(models.Model):
    cantidad = models.PositiveSmallIntegerField(default=1, blank=False, null=False)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Material Ingresado'
        verbose_name_plural = 'Materiales Ingresados'
        constraints = [
            models.UniqueConstraint(
                fields=['material', 'ingreso'],
                name='unique_material_ingreso'
            )
        ]
    
    def __str__(self):
        return f"Ingreso: {self.ingreso.nro_ingreso} - Material: {self.material.descripcion} - Cantidad: {self.cantidad}"

    def save(self, *args, **kwargs):

        if self.pk:
            old_instance = IngresoMaterial.objects.get(pk=self.pk)
            diferencia = self.cantidad - old_instance.cantidad
            self.material.cantidad_existente += diferencia * self.material.cantidad_x_unidad_ingreso
        else:
            self.material.cantidad_existente += self.cantidad * self.material.cantidad_x_unidad_ingreso
        
        self.material.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.material.cantidad_existente -= self.cantidad * self.material.cantidad_x_unidad_ingreso
        self.material.save()
        super().delete(*args, **kwargs)

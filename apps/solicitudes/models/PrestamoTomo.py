from django.db import models

class PrestamoTomo(models.Model):
    fecha_prestamo = models.DateField(blank=True, null=True)
    hora_prestamo = models.TimeField(blank=True, null=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    hora_devolucion = models.TimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Préstamo de Tomo'
        verbose_name_plural = 'Préstamos de Tomos'
    
    def __str__(self):
        return f"Fecha y Hora Préstamo: {self.fecha_prestamo}/{self.hora_prestamo}"

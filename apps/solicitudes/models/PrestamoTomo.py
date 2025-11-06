from django.db import models

class PrestamoTomo(models.Model):
    codigo_prestamo = models.CharField(max_length=5, blank=True, null=True)
    fecha_prestamo = models.DateField(blank=True, null=True)
    hora_prestamo = models.TimeField(blank=True, null=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    hora_devolucion = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Préstamo de Tomo'
        verbose_name_plural = 'Préstamos de Tomos'

    def save(self, *args, **kwargs):
        if not self.codigo_prestamo:
            last = PrestamoTomo.objects.order_by('-codigo_prestamo').first()
            if last:
                num = int(last.codigo_prestamo) + 1
            else:
                num = 1
            self.codigo_prestamo = f"{num:05d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Préstamo {self.codigo_prestamo}, Fecha y Hora {self.fecha_prestamo}/{self.hora_prestamo}"

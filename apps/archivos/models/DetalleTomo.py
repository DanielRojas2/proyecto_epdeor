from django.db import models
from .Tomo import Tomo

class DetalleTomo(models.Model):
    ESTADO_ARCHIVO_CHOICES = (
        ('adjunto', 'Adjunto'),
        ('no adjunto', 'No Adjunto')
    )
    nro_doc = models.SmallIntegerField(default=1, blank=False, null=False)
    nombre_archivo = models.CharField(max_length=25, blank=False, null=False)
    fecha_adjunto = models.DateTimeField(auto_now_add=True)
    nro_fojas = models.SmallIntegerField(blank=True, null=True)
    estado_archivo = models.CharField(max_length=10, blank=True, null=True, choices=ESTADO_ARCHIVO_CHOICES)
    archivo = models.FileField()
    tomo = models.ForeignKey(Tomo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Detalle de Tomo'
        verbose_name_plural = 'Detalles de Tomo'

    def __str__(self):
        return f"Tomo: {self.tomo.nro_tomo} - {self.tomo.titulo}. Archivo: {self.nombre_archivo}"

from django.db import models
from .Tomo import Tomo
from ..functions.guardar_carpeta import get_upload_to
from ..functions.validar_pdf import validate_pdf

class DetalleTomo(models.Model):
    ESTADO_ARCHIVO_CHOICES = (
        ('adjunto', 'Adjunto'),
        ('no adjunto', 'No Adjunto')
    )
    nro_doc = models.SmallIntegerField(default=1, blank=False, null=False)
    nombre_archivo = models.CharField(max_length=200, blank=False, null=False)
    fecha_adjunto = models.DateTimeField(auto_now_add=True)
    nro_fojas = models.SmallIntegerField(blank=True, null=True)
    estado_archivo = models.CharField(max_length=10, blank=True, null=True, choices=ESTADO_ARCHIVO_CHOICES)
    archivo = models.FileField(blank=True, null=False, upload_to=get_upload_to, validators=[validate_pdf])
    tomo = models.ForeignKey(Tomo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Detalle de Tomo'
        verbose_name_plural = 'Detalles de Tomo'
        constraints = [
            models.UniqueConstraint(
                fields=['nro_doc', 'tomo'],
                name='unique_nro_doc_tomo'
            )
        ]
        
    def save(self, *args, **kwargs):
        if self.archivo:
            self.estado_archivo = 'adjunto'
        else:
            self.estado_archivo = 'no adjunto'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tomo: {self.tomo.nro_tomo} - {self.tomo.titulo}. Archivo: {self.nombre_archivo}"

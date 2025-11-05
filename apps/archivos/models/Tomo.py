from django.db import models

class Tomo(models.Model):
    ESTADO_CHOICES = (
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    )
    nro_tomo = models.SmallIntegerField(blank=False, null=False)
    titulo = models.CharField(max_length=75, blank=False, null=False)
    glosa = models.TextField(blank=False, null=False)
    gestion = models.CharField(blank=True, null=True)
    mes = models.CharField(blank=True, null=True)
    fecha_apertura = models.DateField(blank=False, null=False)
    estado = models.CharField(max_length=7, default='activo', choices=ESTADO_CHOICES)
    nro_fojas_total = models.SmallIntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Tomo'
        verbose_name_plural = 'Tomos'
        constraints = [
            models.UniqueConstraint(
                fields=['nro_tomo', 'titulo'],
                name='unique_nro_tomo_titulo'
            )
        ]
    
    def __str__(self):
        return f"Tomo: {self.nro_tomo} {self.titulo}"

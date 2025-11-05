from django.db import models

class Nivel(models.Model):
    nro_nivel = models.SmallIntegerField(blank=False, null=False)
    
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'
    
    def __str__(self):
        return f"{self.nro_nivel}"

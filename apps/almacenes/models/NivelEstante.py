from django.db import models
from .Estante import Estante
from .Nivel import Nivel

class NivelEstante(models.Model):
    estante = models.ForeignKey(Estante, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    espacio_disponible = models.SmallIntegerField(default=100)
    
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nivel de Estante'
        verbose_name = 'Niveles de Estante'
        constraints = [
            models.UniqueConstraint(
                fields=['estante', 'nivel'],
                name='unique_estante_nivel'
            )
        ]
    
    def __str__(self):
        return f"Nivel {self.nivel} de estante {self.estante.nro_estante} de almacen {self.estante.almacen.nro_almacen} de {self.estante.almacen.tipo_almacen}"

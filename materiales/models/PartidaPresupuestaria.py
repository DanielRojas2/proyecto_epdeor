from django.db import models

class PartidaPresupuestaria(models.Model):
    partida = models.CharField(max_length=5, blank=False, null=False)
    categoria = models.CharField(max_length=75, blank=False, null=False)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partida Presupuestaria'
        verbose_name_plural = 'Partidas Presupuestarias'
        constraints = [
            models.UniqueConstraint(
                fields=['partida', 'categoria'],
                name='unique_partida_categoria'
            )
        ]
    
    def __str__(self):
        return f"Partida: {self.partida} - Categoria: {self.categoria}"

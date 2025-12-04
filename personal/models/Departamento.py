from django.db import models

class Departamento(models.Model):
    departamento = models.CharField(
        max_length=100, unique=True,
        blank=False, null=False
    )
    jefe = models.OneToOneField(
        "Personal", on_delete=models.SET_NULL, null=True,
        blank=True, related_name="departamento_que_dirige"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['creado']

    def __str__(self):
        return self.departamento

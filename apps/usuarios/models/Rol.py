from django.db import models

class Rol(models.Model):
    rol = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['rol']

    def __str__(self):
        return self.rol

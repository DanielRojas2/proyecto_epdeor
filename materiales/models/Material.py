import re
from django.db import models
from .PartidaPresupuestaria import PartidaPresupuestaria

class Material(models.Model):
    TIPO_MATERIAL_CHOICES = (
        ('material de escritorio', 'material de escritorio'),
        ('material de limpieza', 'material de limpieza'),
        ('material de mantenimiento', 'material de mantenimiento')
    )
    codigo_material = models.CharField(max_length=14, blank=False, null=False)
    descripcion = models.CharField(max_length=50, blank=False, null=False, unique=True)
    cantidad_minima = models.PositiveSmallIntegerField(default=1, blank=False, null=False)
    cantidad_existente = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    unidad_ingreso = models.CharField(max_length=35, blank=False, null=False)
    cantidad_x_unidad_ingreso = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    volumen = models.CharField(max_length=25, blank=False, null=False, default='N/A')
    unidad_salida = models.CharField(max_length=35, blank=False, null=False)
    tipo_material = models.CharField(max_length=25, blank=False, null=False)
    partida = models.ForeignKey(PartidaPresupuestaria, on_delete=models.CASCADE)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

    def __str__(self):
        return f"Codigo: {self.codigo_material} - Material: {self.descripcion}"

    def save(self, *args, **kwargs):
        if not self.codigo_material:
            self.codigo_material = self.generar_codigo_material()
        super().save(*args, **kwargs)

    def generar_codigo_material(self):
        """
        Genera código automático mejorado que maneja palabras de conexión.
        """
        palabras_ignorar = ['de', 'del', 'la', 'las', 'los', 'el', 'y', 'e', 'o', 'u', 
                        'en', 'por', 'para', 'con', 'sin', 'sobre', 'bajo']
        
        categoria_limpia = re.sub(r'[^\w\s]', '', self.partida.categoria)
        palabras = categoria_limpia.split()
        
        palabras_filtradas = [
            palabra for palabra in palabras 
            if palabra.lower() not in palabras_ignorar and palabra.strip()
        ]
        
        if len(palabras_filtradas) == 0:
            iniciales = self.partida.categoria[:2].upper()
        elif len(palabras_filtradas) == 1:
            iniciales = palabras_filtradas[0][:2].upper()
        elif len(palabras_filtradas) == 2:
            iniciales = palabras_filtradas[0][0].upper() + palabras_filtradas[1][0].upper()
        else:
            iniciales = "".join(p[0].upper() for p in palabras_filtradas)
        
        partida_num = self.partida.partida
        if len(partida_num) >= 3:
            ultimos_tres = partida_num[-3:]
            cd = ultimos_tres.rstrip('0').zfill(2)
        else:
            cd = partida_num.zfill(2)
        
        materiales_misma_partida = Material.objects.filter(partida=self.partida)
        correlativo = materiales_misma_partida.count() + 1
        ef = str(correlativo).zfill(2)
        
        codigo = f"{iniciales}-{cd}-{ef}-{partida_num}"
        return codigo

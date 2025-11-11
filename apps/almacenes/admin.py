from django.contrib import admin
from .models.Almacen import Almacen
from .models.Estante import Estante
from .models.Nivel import Nivel
from .models.NivelEstante import NivelEstante

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('id', 'nro_almacen', 'tipo_almacen', 'ubicacion', 'estado_almacen', 'creado', 'actualizado')
    list_filter = ('tipo_almacen', 'estado_almacen')
    search_fields = ('nro_almacen', 'tipo_almacen', 'ubicacion')
    ordering = ('nro_almacen', 'tipo_almacen')

@admin.register(Estante)
class EstanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nro_estante', 'almacen', 'creado', 'actualizado')
    list_filter = ('almacen__tipo_almacen',)
    search_fields = ('nro_estante', 'almacen__nro_almacen')
    ordering = ('almacen', 'nro_estante')

@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('id', 'nro_nivel', 'creado', 'actualizado')
    ordering = ('nro_nivel',)

@admin.register(NivelEstante)
class NivelEstanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'estante', 'nivel', 'espacio_disponible', 'creado', 'actualizado')
    list_filter = ('estante__almacen__tipo_almacen',)
    search_fields = (
        'estante__nro_estante',
        'estante__almacen__nro_almacen',
        'nivel__nro_nivel'
    )
    ordering = ('estante', 'nivel')

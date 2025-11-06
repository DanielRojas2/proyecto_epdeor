from django.contrib import admin
from .models.PartidaPresupuestaria import PartidaPresupuestaria
from .models.UdM import UdM
from .models.Material import Material

@admin.register(PartidaPresupuestaria)
class PartidaPresupuestariaAdmin(admin.ModelAdmin):
    list_display = ('partida', 'categoria', 'creado', 'actualizado')
    search_fields = ('partida', 'categoria')
    list_filter = ('creado', 'actualizado')
    ordering = ('partida',)
    
@admin.register(UdM)
class UdMAdmin(admin.ModelAdmin):
    list_display = ('unidad_de_medida', 'presentacion', 'creado', 'actualizado')
    search_fields = ('unidad_de_medida', 'presentacion')
    ordering = ('unidad_de_medida',)
    
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descripcion', 'partida', 'udm',
        'nivel_minimo', 'cantidad_existente',
        'creado', 'actualizado'
    )
    search_fields = ('descripcion', 'partida__partida', 'udm__unidad_de_medida')
    list_filter = ('partida', 'udm')
    ordering = ('descripcion',)

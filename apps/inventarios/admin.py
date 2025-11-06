from django.contrib import admin
from .models.AsignacionTomo import AsignacionTomo
from .models.AsignacionMaterial import AsignacionMaterial

@admin.register(AsignacionTomo)
class AsignacionTomoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tomo',
        'estante_almacen',
        'estado_tomo',
        'espacio_ocupado',
        'fecha_asignacion',
        'hora_asigancion',
    )
    list_filter = ('estado_tomo', 'estante_almacen', 'fecha_asignacion')
    search_fields = ('tomo__titulo', 'estante_almacen__estante__nro_estante')
    ordering = ('-fecha_asignacion', '-hora_asigancion')
    
@admin.register(AsignacionMaterial)
class AsignacionMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'material_asignado',
        'estante_almacen',
        'cantidad_asignacion',
        'espacio_ocupado',
        'fecha_asignacion',
        'hora_asigancion',
    )
    search_fields = (
        'material_asignado__descripcion',
        'estante_almacen__estante__nro_estante',
        'estante_almacen__nivel__nro_nivel',
    )
    list_filter = (
        'fecha_asignacion',
        'estante_almacen',
        'material_asignado',
    )
    ordering = ('-fecha_asignacion', '-hora_asigancion')

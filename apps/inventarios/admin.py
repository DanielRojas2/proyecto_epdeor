from django.contrib import admin
from .models.AsignacionTomo import AsignacionTomo

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

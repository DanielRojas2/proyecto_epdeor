from django.contrib import admin
from .models.Tomo import Tomo
from .models.DetalleTomo import DetalleTomo

@admin.register(Tomo)
class TomoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nro_tomo',
        'titulo',
        'glosa',
        'gestion',
        'mes',
        'fecha_apertura',
        'estado',
        'nro_fojas_total',
    )
    list_filter = ('estado', 'gestion', 'mes')
    search_fields = ('titulo', 'nro_tomo', 'glosa')
    ordering = ('nro_tomo', 'fecha_apertura')
    readonly_fields = ('gestion', 'mes')

    fieldsets = (
        ('Información del Tomo', {
            'fields': ('nro_tomo', 'titulo', 'glosa', 'estado')
        }),
        ('Fechas y Control', {
            'fields': ('fecha_apertura', 'gestion', 'mes')
        }),
        ('Datos Adicionales', {
            'fields': ('nro_fojas_total',)
        }),
    )


@admin.register(DetalleTomo)
class DetalleTomoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tomo',
        'nro_doc',
        'nombre_archivo',
        'fecha_adjunto',
        'nro_fojas',
        'estado_archivo',
    )
    list_filter = ('estado_archivo', 'tomo__estado', 'tomo__gestion')
    search_fields = ('nombre_archivo', 'tomo__titulo', 'tomo__nro_tomo')
    ordering = ('tomo', 'nro_doc')
    readonly_fields = ('fecha_adjunto', 'estado_archivo')

    fieldsets = (
        ('Documento del Tomo', {
            'fields': ('tomo', 'nro_doc', 'nombre_archivo', 'nro_fojas')
        }),
        ('Archivo', {
            'fields': ('archivo', 'estado_archivo', 'fecha_adjunto')
        }),
    )

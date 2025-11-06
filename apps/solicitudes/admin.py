from django.contrib import admin
from .models.PrestamoTomo import PrestamoTomo
from .models.DetallePrestamo import DetallePrestamo
from .models.SolicitudPrestamo import SolicitudPrestamo


@admin.register(PrestamoTomo)
class PrestamoTomoAdmin(admin.ModelAdmin):
    list_display = ('codigo_prestamo', 'fecha_prestamo', 'hora_prestamo', 'fecha_devolucion', 'hora_devolucion')
    search_fields = ('codigo_prestamo',)
    list_filter = ('fecha_prestamo',)


@admin.register(DetallePrestamo)
class DetallePrestamoAdmin(admin.ModelAdmin):
    list_display = ('codigo_prestamo', 'tomo_solicitado', 'estado_detalle_tomo')
    list_filter = ('estado_detalle_tomo',)
    search_fields = ('codigo_prestamo__codigo_prestamo', 'tomo_solicitado__tomo__titulo')


@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo_prestamo', 'estado_solicitud', 'rol_solicitud')
    list_filter = ('estado_solicitud', 'rol_solicitud')
    search_fields = ('usuario__username', 'codigo_prestamo__codigo_prestamo')

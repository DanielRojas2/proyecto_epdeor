from django.urls import path
from .views import solicitud_views
from .views import atencion_views
from .views import entrega_views
from .views.pdf_views import NotaSolicitudPDFView, DetalleSolicitudPDFView

app_name = "solicitudes"

urlpatterns = [
    path("solicitar/", solicitud_views.solicitar_material_view, name="solicitar_material"),
    path("carrito-parcial/", solicitud_views.carrito_parcial_view, name="carrito_parcial"),
    path("agregar/<int:material_id>/", solicitud_views.agregar_al_carrito, name="agregar"),
    path("actualizar/<int:material_id>/", solicitud_views.actualizar_carrito, name="actualizar"),
    path("eliminar/<int:material_id>/", solicitud_views.eliminar_del_carrito, name="eliminar"),
    path("generar/", solicitud_views.generar_solicitud, name="generar"),

    path("nota-pdf/<int:pk>/", NotaSolicitudPDFView.as_view(), name="nota_pdf"),
    path("detalle-pdf/<int:pk>/", DetalleSolicitudPDFView.as_view(), name="detalle_pdf"),

    path("pendientes/", atencion_views.solicitudes_pendientes_view, name="pendientes"),
    path("atender/<int:solicitud_id>/", atencion_views.atender_solicitud_view, name="atender"),
    path("detalle/modificar/<int:detalle_id>/", atencion_views.modificar_detalle_solicitud, name="modificar_detalle"),
    path("aprobar/<int:solicitud_id>/", atencion_views.aprobar_solicitud, name="aprobar"),
    path("rechazar/<int:solicitud_id>/", atencion_views.rechazar_solicitud, name="rechazar"),

    path("entregas/", entrega_views.solicitudes_aprobadas_view, name="entregas"),
    path("entrega/<int:solicitud_id>/", entrega_views.entregar_material_view, name="entregar"),
    path("entrega/registrar/<int:solicitud_id>/", entrega_views.registrar_entrega, name="registrar_entrega"),
]

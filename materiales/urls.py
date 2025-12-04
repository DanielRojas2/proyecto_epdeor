from django.urls import path
from .views.MaterialViews import MaterialView, CrearMaterialView, MaterialesReportListView
from .views.PartidaView import PartidasPresupuestariasView, CrearPartidaPresupuestariaView
from .views.IngresoMaterialView import (
    MaterialesListView, ProveedoresListView,
    CrearProveedorView, RegistrarIngresoView,
    IngresoMaterialView
)
from .views.AlmacenView import AlmacenesView, CrearAlmacenView
from .views.IngresoReportView import IngresoPDFView

app_name = 'materiales'

urlpatterns = [
    path('', MaterialView.as_view(), name='material'),
    path('materiales-list/', MaterialesReportListView.as_view(), name='materiales_lista'),
    path('ingresar-material/', IngresoMaterialView.as_view(), name='ingresar_material'),
    path('crear-material/', CrearMaterialView.as_view(), name='crear_material'),
    path('partidas-presupuestarias/', PartidasPresupuestariasView.as_view(), name='partidas_presupuestarias'),
    path('crear-partida/', CrearPartidaPresupuestariaView.as_view(), name='crear_partida'),
    path('materiales/', MaterialesListView.as_view(), name='materiales_list'),
    path('proveedores/', ProveedoresListView.as_view(), name='proveedores_list'),
    path('crear-proveedor/', CrearProveedorView.as_view(), name='crear_proveedor'),
    path('registrar-ingreso/', RegistrarIngresoView.as_view(), name='registrar_ingreso'),

    path('ingresos/<int:pk>/reporte/', IngresoPDFView.as_view(), name='ingreso_reporte_pdf'),

    path('almacenes/', AlmacenesView.as_view(), name='almacenes'),
    path('crear-almacen/', CrearAlmacenView.as_view(), name='crear-almacen'),
]

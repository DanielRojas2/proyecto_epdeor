from django.urls import path
from .views.asignacion_tomo_views import (
    asignacion_tomo_list,
    asignacion_tomo_create,
    asignacion_tomo_update,
    asignacion_tomo_delete,
)

urlpatterns = [
    path('inventarios/', asignacion_tomo_list, name='inventario_tomos'),
    path('asignaciones/nueva/', asignacion_tomo_create, name='asignacion_tomo_create'),
    path('asignaciones/<int:pk>/editar/', asignacion_tomo_update, name='asignacion_tomo_update'),
    path('asignaciones/<int:pk>/eliminar/', asignacion_tomo_delete, name='asignacion_tomo_delete'),
]

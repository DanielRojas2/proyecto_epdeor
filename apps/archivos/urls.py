from django.urls import path
from .views.tomo_views import tomos_list, tomo_create, tomo_update, tomo_delete
from .views.detalle_tomo_views import (
    detalle_tomo_list, detalle_tomo_create, detalle_tomo_edit, detalle_tomo_delete
)

urlpatterns = [
    path('tomos/', tomos_list, name='tomos'),
    path('tomos/nuevo/', tomo_create, name='tomo_create'),
    path('tomos/<int:pk>/editar/', tomo_update, name='tomo_update'),
    path('tomos/<int:pk>/eliminar/', tomo_delete, name='tomo_delete'),

    path('tomo/<int:tomo_id>/detalles/', detalle_tomo_list, name='detalle_tomo_list'),
    path('detalle_tomo/create/<int:tomo_id>/', detalle_tomo_create, name='detalle_tomo_create'),
    path('detalle_tomo/edit/<int:pk>/', detalle_tomo_edit, name='detalle_tomo_edit'),
    path('detalle_tomo/delete/<int:pk>/', detalle_tomo_delete, name='detalle_tomo_delete'),
]

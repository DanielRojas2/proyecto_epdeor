from django.urls import path
from .views.almacen import almacen, almacen_create, almacen_delete, almacen_update
from .views.almacen_detalle import almacen_detalle
from .views.estante_views import estante_create
from .views.nivel_estante_views import nivel_estante_create
from .views.nivel_views import nivel_create

urlpatterns = [
    path('almacenes/', almacen, name='almacenes'),
    path('almacenes/crear/', almacen_create, name='almacen_create'),
    path('almacenes/editar/<int:pk>/', almacen_update, name='almacen_update'),
    path('almacenes/eliminar/<int:pk>/', almacen_delete, name='almacen_delete'),
    path('almacen/<int:pk>/almacen-detalle/', almacen_detalle, name='almacen_detalle'),
    path('almacen/<int:almacen_id>/estante/create/', estante_create, name='estante_create'),
    path('nivel_estante/create/<int:estante_id>/', nivel_estante_create, name='nivel_estante_create'),
    path('nivel/create/', nivel_create, name='nivel_create'),
]

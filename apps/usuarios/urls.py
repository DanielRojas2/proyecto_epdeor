from django.urls import path
from .views.usuario_views import usuario_list, usuario_create, usuario_update, usuario_delete

urlpatterns = [
    path('usuarios/', usuario_list, name='usuarios'),
]

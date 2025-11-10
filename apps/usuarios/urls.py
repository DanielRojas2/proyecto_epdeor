from django.urls import path
from .views.usuario_views import usuario_list

urlpatterns = [
    path('usuarios/', usuario_list, name='usuarios'),
]

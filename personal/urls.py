from django.urls import path
from .views.personal_views import usuarios, toggle_estado_usuario

urlpatterns = [
    path('', usuarios, name='usuarios'),
    path('toggle/<int:id>/', toggle_estado_usuario, name='toggle_estado_usuario'),
]

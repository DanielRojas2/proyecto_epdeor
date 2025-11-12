from django.urls import path
from .views.solicitud_tomo_views import solicitar_tomo

urlpatterns = [
    path('solitictar-tomos/', solicitar_tomo, name='solicitar_tomo'),
]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

urlpatterns = [
    path('iniciar-sesion/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=LoginForm
    ), name='iniciar_sesion'),
    path('cerrar-sesion/', LogoutView.as_view(), name='cerrar_sesion'),
]

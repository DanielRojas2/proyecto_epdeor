from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from solicitudes.models import SolicitudMaterial

class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "inicio/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solicitudes"] = (
            SolicitudMaterial.objects
            .filter(creado_por=self.request.user)
            .select_related("dirigido_a")
            .order_by("-fecha_solicitud", "-hora_solicitud")[:3]
        )
        return context

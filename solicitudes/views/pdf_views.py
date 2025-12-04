# solicitudes/views/pdf_views.py
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

from ..models import SolicitudMaterial, DetalleSolicitudMaterial
from personal.models import Personal

class NotaSolicitudPDFView(View):
    def get(self, request, pk):
        solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
        try:
            personal = Personal.objects.get(usuario=solicitud.creado_por)
        except Personal.DoesNotExist:
            personal = None

        template = get_template("solicitudes/reportes/nota_interna.html")
        context = {
            "solicitud": solicitud,
            "personal": personal,
            "request": request,
        }
        html = template.render(context)

        response = HttpResponse(content_type="application/pdf")
        filename = f"nota_solicitud_{solicitud.codigo_solicitud}.pdf"
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error al generar el PDF de la nota interna", status=500)

        return response


class DetalleSolicitudPDFView(View):
    def get(self, request, pk):
        solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
        detalles = DetalleSolicitudMaterial.objects.select_related("material").filter(solicitud=solicitud)
        try:
            personal = Personal.objects.get(usuario=solicitud.creado_por)
        except Personal.DoesNotExist:
            personal = None

        template = get_template("solicitudes/reportes/detalle_solicitud.html")
        context = {
            "solicitud": solicitud,
            "detalles": detalles,
            "personal": personal,
            "request": request,
        }
        html = template.render(context)

        response = HttpResponse(content_type="application/pdf")
        filename = f"detalle_solicitud_{solicitud.codigo_solicitud}.pdf"
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error al generar el PDF del detalle de la solicitud", status=500)

        return response

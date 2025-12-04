from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from ..models.Ingreso import Ingreso
from ..models.IngresoMaterial import IngresoMaterial

class IngresoPDFView(View):
    def get(self, request, pk):
        ingreso = get_object_or_404(Ingreso, pk=pk)
        materiales_ingresados = IngresoMaterial.objects.select_related('material').filter(ingreso=ingreso)

        template = get_template('material/reportes/ingreso_pdf.html')
        context = {
            'ingreso': ingreso,
            'materiales_ingresados': materiales_ingresados,
            'request': request,
        }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        filename = f'ingreso_{ingreso.nro_ingreso}.pdf'
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response

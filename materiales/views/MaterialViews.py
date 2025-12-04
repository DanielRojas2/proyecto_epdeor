import json
from django.db.models import Q
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from ..models.Material import Material
from ..models.PartidaPresupuestaria import PartidaPresupuestaria

class MaterialView(TemplateView):
    template_name = 'material/material.html'

class MaterialesReportListView(View):
    def get(self, request):
        try:
            search = request.GET.get('search', '')
            tipo_material = request.GET.get('tipo_material', '')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 5))
            
            materiales = Material.objects.select_related('partida').all()
            
            if search:
                materiales = materiales.filter(
                    Q(descripcion__icontains=search) |
                    Q(codigo_material__icontains=search)
                )
            
            if tipo_material:
                materiales = materiales.filter(tipo_material=tipo_material)
            
            paginator = Paginator(materiales, page_size)
            materiales_page = paginator.get_page(page)
            
            materiales_data = []
            for material in materiales_page:
                materiales_data.append({
                    'codigo_material': material.codigo_material,
                    'descripcion': material.descripcion,
                    'partida': material.partida.partida,
                    'cantidad_existente': material.cantidad_existente,
                    'unidad_ingreso': material.unidad_ingreso,
                    'cantidad_x_unidad_ingreso': material.cantidad_x_unidad_ingreso,
                    'volumen': material.volumen,
                    'unidad_salida': material.unidad_salida,
                    'tipo_material': material.tipo_material,
                })
            
            return JsonResponse({
                'success': True,
                'materiales': materiales_data,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'has_previous': materiales_page.has_previous(),
                    'has_next': materiales_page.has_next(),
                    'previous_page_number': materiales_page.previous_page_number() if materiales_page.has_previous() else None,
                    'next_page_number': materiales_page.next_page_number() if materiales_page.has_next() else None,
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CrearMaterialView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            try:
                partida_id = data.get('partida')
                partida = PartidaPresupuestaria.objects.get(id=partida_id)
            except PartidaPresupuestaria.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'La partida presupuestaria no existe'
                }, status=400)
            
            material = Material(
                descripcion=data.get('descripcion'),
                cantidad_minima=data.get('cantidad_minima', 1),
                unidad_ingreso=data.get('unidad_ingreso'),
                cantidad_x_unidad_ingreso=data.get('cantidad_x_unidad_ingreso', 1),
                volumen=data.get('volumen', 'N/A'),
                unidad_salida=data.get('unidad_salida'),
                tipo_material=data.get('tipo_material'),
                partida=partida
            )
            
            material.save()
            
            return JsonResponse({
                'success': True,
                'material': {
                    'id': material.id,
                    'codigo_material': material.codigo_material,
                    'descripcion': material.descripcion,
                    'partida': material.partida.partida,
                    'categoria': material.partida.categoria
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

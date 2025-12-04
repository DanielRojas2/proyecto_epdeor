import json
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models.Material import Material
from ..models.Proveedor import Proveedor
from ..models.Ingreso import Ingreso
from ..models.IngresoMaterial import IngresoMaterial

class IngresoMaterialView(TemplateView):
    template_name = 'material/ingreso_material.html'


@method_decorator(csrf_exempt, name='dispatch')
class MaterialesListView(View):
    def get(self, request):
        try:
            search = request.GET.get('search', '')
            materiales = Material.objects.all()
            
            if search:
                materiales = materiales.filter(descripcion__icontains=search)
            
            materiales_data = materiales.values(
                'id', 'codigo_material', 'descripcion', 'unidad_ingreso', 
                'volumen', 'cantidad_x_unidad_ingreso', 'partida__partida', 'partida__categoria'
            )[:50]
            
            return JsonResponse({
                'success': True,
                'materiales': list(materiales_data)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ProveedoresListView(View):
    def get(self, request):
        try:
            proveedores = Proveedor.objects.all().values('id', 'proveedor', 'nit')
            return JsonResponse({
                'success': True,
                'proveedores': list(proveedores)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class CrearProveedorView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            proveedor_nombre = data.get('proveedor')
            nit = data.get('nit')
            
            if not proveedor_nombre or not nit:
                return JsonResponse({
                    'success': False,
                    'error': 'Proveedor y NIT son campos requeridos'
                }, status=400)
            
            nuevo_proveedor = Proveedor(proveedor=proveedor_nombre, nit=nit)
            nuevo_proveedor.save()
            
            return JsonResponse({
                'success': True,
                'proveedor': {
                    'id': nuevo_proveedor.id,
                    'proveedor': nuevo_proveedor.proveedor,
                    'nit': nuevo_proveedor.nit
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RegistrarIngresoView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            ingreso = Ingreso(
                nro_ingreso=data.get('nro_ingreso'),
                fecha_ingreso=data.get('fecha_ingreso'),
                factura=data.get('factura'),
                h_ruta=data.get('h_ruta'),
                orden_compra=data.get('orden_compra'),
                proveedor_id=data.get('proveedor_id'),
                almacen_id=data.get('almacen_id')
            )
            ingreso.save()
            
            materiales_ingresados = data.get('materiales_ingresados', [])
            for material_data in materiales_ingresados:
                ingreso_material = IngresoMaterial(
                    cantidad=material_data['cantidad'],
                    material_id=material_data['material_id'],
                    ingreso=ingreso
                )
                ingreso_material.save()

            pdf_url = reverse('materiales:ingreso_reporte_pdf', args=[ingreso.id])
            redirect_url = reverse('materiales:material')  # URL principal de materiales
            
            return JsonResponse({
                'success': True,
                'ingreso_id': ingreso.id,
                'pdf_url': pdf_url,
                'redirect_url': redirect_url,
                'message': 'Ingreso registrado exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
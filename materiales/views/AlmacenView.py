import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models.Almacen import Almacen

class AlmacenesView(View):
    def get(self, request):
        try:
            almacenes = Almacen.objects.all().values('id', 'nro_almacen', 'descripcion', 'ubicacion')
            return JsonResponse({
                'success': True,
                'almacenes': list(almacenes)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CrearAlmacenView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nro_almacen = data.get('nro_almacen')
            descripcion = data.get('descripcion')
            ubicacion = data.get('ubicacion')

            if not nro_almacen or not descripcion or not ubicacion:
                return JsonResponse({
                    'success': False,
                    'error': 'Nro. de almacén, descripción y ubicación son campos requeridos'
                }, status=400)

            nuevo_almacen = Almacen(
                nro_almacen=nro_almacen,
                descripcion=descripcion,
                ubicacion=ubicacion
            )
            nuevo_almacen.save()

            return JsonResponse({
                'success': True,
                'almacen': {
                    'id': nuevo_almacen.id,
                    'nro_almacen': nuevo_almacen.nro_almacen,
                    'descripcion': nuevo_almacen.descripcion,
                    'ubicacion': nuevo_almacen.ubicacion
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

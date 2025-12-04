import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models.PartidaPresupuestaria import PartidaPresupuestaria

@method_decorator(csrf_exempt, name='dispatch')
class CrearPartidaPresupuestariaView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            partida_numero = data.get('partida')
            categoria = data.get('categoria')            
            if not partida_numero or not categoria:
                return JsonResponse({
                    'success': False,
                    'error': 'Partida y categoría son campos requeridos'
                }, status=400)            
            if PartidaPresupuestaria.objects.filter(partida=partida_numero, categoria=categoria).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Esta partida presupuestaria ya existe'
                }, status=400)            
            nueva_partida = PartidaPresupuestaria(
                partida=partida_numero,
                categoria=categoria
            )
            nueva_partida.save()
            
            return JsonResponse({
                'success': True,
                'partida': {
                    'id': nueva_partida.id,
                    'partida': nueva_partida.partida,
                    'categoria': nueva_partida.categoria
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

class PartidasPresupuestariasView(View):
    def get(self, request):
        try:
            partidas = PartidaPresupuestaria.objects.all().values('id', 'partida', 'categoria')
            return JsonResponse({
                'success': True,
                'partidas': list(partidas)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

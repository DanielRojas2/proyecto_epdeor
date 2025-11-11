from django.http import JsonResponse
from ..models.Nivel import Nivel

def nivel_create(request):
    if request.method == 'POST':
        nro_nivel = (Nivel.objects.order_by('-nro_nivel').first().nro_nivel + 1) if Nivel.objects.exists() else 1
        nivel = Nivel.objects.create(nro_nivel=nro_nivel)
        return JsonResponse({'success': True, 'nivel': nivel.nro_nivel})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

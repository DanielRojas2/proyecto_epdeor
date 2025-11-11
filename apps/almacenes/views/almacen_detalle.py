from django.shortcuts import render, get_object_or_404
from ..models.Almacen import Almacen
from ..models.Estante import Estante
from ..models.Nivel import Nivel
from ..models.NivelEstante import NivelEstante

def almacen_detalle(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    estantes = Estante.objects.filter(almacen=almacen).order_by('nro_estante')
    niveles_por_estante = {
        estante.id: NivelEstante.objects.filter(estante=estante).order_by('nivel__nro_nivel')
        for estante in estantes
    }
    return render(request, 'detalles_almacen/detalles_almacen.html', {
        'almacen': almacen,
        'estantes': estantes,
        'niveles_por_estante': niveles_por_estante
    })

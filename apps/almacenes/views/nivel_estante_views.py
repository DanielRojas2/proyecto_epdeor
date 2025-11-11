from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ..models.Estante import Estante
from ..forms.NivelEstanteForm import NivelEstanteForm

def nivel_estante_create(request, estante_id):
    estante = get_object_or_404(Estante, pk=estante_id)
    if request.method == 'POST':
        form = NivelEstanteForm(request.POST, estante=estante)
        if form.is_valid():
            nivel_estante = form.save(commit=False)
            nivel_estante.estante = estante
            nivel_estante.save()
            return redirect('almacen_detalle', pk=estante.almacen.id)
    else:
        form = NivelEstanteForm(estante=estante)
    return render(request, 'detalles_almacen/partials/nivel_estante_form.html', {
        'form': form,
        'estante': estante,
        'title': f'Asignar nivel a Estante {estante.nro_estante}'
    })

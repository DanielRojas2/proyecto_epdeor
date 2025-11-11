from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ..models.Almacen import Almacen
from ..forms.EstanteForm import EstanteForm

def estante_create(request, almacen_id):
    almacen = get_object_or_404(Almacen, pk=almacen_id)
    if request.method == 'POST':
        form = EstanteForm(request.POST)
        if form.is_valid():
            estante = form.save(commit=False)
            estante.almacen = almacen
            estante.save()
            return redirect('almacen_detalle', pk=almacen.id)
    else:
        form = EstanteForm()
    return render(request, 'detalles_almacen/partials/estante_form.html', {
        'form': form,
        'almacen': almacen,
        'title': f'Agregar estante a {almacen}'
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from ..models.Tomo import Tomo
from ..models.DetalleTomo import DetalleTomo
from ..forms.DetalleTomoForm import DetalleTomoForm

def detalle_tomo_list(request, tomo_id):
    tomo = get_object_or_404(Tomo, pk=tomo_id)
    detalles = DetalleTomo.objects.filter(tomo=tomo).order_by('nro_doc')

    estados = DetalleTomo.objects.values_list('estado_archivo', flat=True).distinct()
    data = [
        {
            'id': d.id,
            'nro_doc': d.nro_doc,
            'nombre_archivo': d.nombre_archivo,
            'nro_fojas': d.nro_fojas or 0,
            'estado_archivo': d.estado_archivo,
            'fecha_adjunto': d.fecha_adjunto.strftime('%d/%m/%Y %H:%M'),
            'url_archivo': d.archivo.url if d.archivo else '',
            'url_edit': f"/detalle_tomo/edit/{d.id}/",
            'url_delete': f"/detalle_tomo/delete/{d.id}/",
        }
        for d in detalles
    ]

    context = {
        'tomo': tomo,
        'detalles_data': data,
        'estados': estados,
    }
    return render(request, 'detalles_tomo/detalle_tomo_list.html', context)


def detalle_tomo_create(request, tomo_id):
    tomo = get_object_or_404(Tomo, pk=tomo_id)
    if request.method == 'POST':
        form = DetalleTomoForm(request.POST, request.FILES)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.tomo = tomo
            detalle.save()
            messages.success(request, 'Archivo adjuntado correctamente.')
            return redirect('detalle_tomo_list', tomo_id=tomo.id)
    else:
        form = DetalleTomoForm()

    return render(request, 'detalles_tomo/detalle_tomo_form.html', {
        'form': form,
        'tomo': tomo,
        'action_url': reverse('detalle_tomo_create', args=[tomo.id])
    })


def detalle_tomo_edit(request, pk):
    detalle = get_object_or_404(DetalleTomo, pk=pk)
    if request.method == 'POST':
        form = DetalleTomoForm(request.POST, request.FILES, instance=detalle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Detalle actualizado correctamente.')
            return redirect('detalle_tomo_list', tomo_id=detalle.tomo.id)
    else:
        form = DetalleTomoForm(instance=detalle)

    return render(request, 'detalles_tomo/detalle_tomo_form.html', {
        'form': form,
        'detalle': detalle,
        'tomo': detalle.tomo,
        'action_url': reverse('detalle_tomo_edit', args=[detalle.id])
    })

def detalle_tomo_delete(request, pk):
    detalle = get_object_or_404(DetalleTomo, pk=pk)
    tomo_id = detalle.tomo.id
    detalle.delete()
    messages.success(request, 'Archivo eliminado correctamente.')
    return redirect('detalle_tomo_list', tomo_id=tomo_id)

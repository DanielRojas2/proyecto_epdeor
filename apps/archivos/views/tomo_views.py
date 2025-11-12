from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from ..models.Tomo import Tomo
from ..forms.TomoForm import TomoForm

def tomos_list(request):
    tomos_qs = Tomo.objects.all().order_by('nro_tomo')

    gestiones = Tomo.objects.values_list('gestion', flat=True).distinct()
    meses = Tomo.objects.values_list('mes', flat=True).distinct()
    estados = Tomo.objects.values_list('estado', flat=True).distinct()

    tomos_data = []
    for t in tomos_qs:
        tomos_data.append({
            'id': t.id,
            'nro_tomo': t.nro_tomo,
            'titulo': t.titulo,
            'glosa': t.glosa,
            'gestion': t.gestion or "",
            'mes': t.mes or "",
            'fecha_apertura': t.fecha_apertura.strftime("%Y-%m-%d") if t.fecha_apertura else "",
            'nro_fojas_total': t.nro_fojas_total or 0,
            'estado': t.estado,
            'url_edit': reverse('tomo_update', args=[t.id]),
            'url_delete': reverse('tomo_delete', args=[t.id]),
            'url_detalle': reverse('detalle_tomo_list', args=[t.id]),
        })

    form = TomoForm()

    return render(request, 'tomos/tomos_list.html', {
        'tomos': tomos_qs,
        'tomos_data': tomos_data,
        'gestiones': gestiones,
        'meses': meses,
        'estados': estados,
        'form': form,
    })

def tomo_create(request):
    if request.method == 'POST':
        form = TomoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tomo creado correctamente ✅")
            return redirect('tomos')
    else:
        form = TomoForm()
    return render(request, 'tomos/tomo_form.html', {
        'form': form,
        'title': 'Nuevo Tomo',
        'action_url': reverse('tomo_create')
    })


def tomo_update(request, pk):
    tomo = get_object_or_404(Tomo, pk=pk)
    if request.method == 'POST':
        form = TomoForm(request.POST, instance=tomo)
        if form.is_valid():
            form.save()
            messages.success(request, "Tomo actualizado correctamente ✏️")
            return redirect('tomos')
    else:
        form = TomoForm(instance=tomo)
    return render(request, 'tomos/tomo_form.html', {
        'form': form,
        'title': f'Editar Tomo #{tomo.nro_tomo}',
        'action_url': reverse('tomo_update', args=[pk])
    })


def tomo_delete(request, pk):
    tomo = get_object_or_404(Tomo, pk=pk)
    tomo.delete()
    messages.success(request, "Tomo eliminado correctamente 🗑️")
    return redirect('tomos')

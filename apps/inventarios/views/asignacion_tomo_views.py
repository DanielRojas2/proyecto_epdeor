from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from ..models.AsignacionTomo import AsignacionTomo
from ..forms.AsignacionTomoForm import AsignacionTomoForm
from ...almacenes.models.NivelEstante import NivelEstante
from ...archivos.models.Tomo import Tomo


def asignacion_tomo_list(request):
    estante_id = request.GET.get('estante')
    tomo_id = request.GET.get('tomo')

    asignaciones = AsignacionTomo.objects.select_related('estante_almacen', 'tomo').order_by('-fecha_asignacion')

    if estante_id:
        asignaciones = asignaciones.filter(estante_almacen__id=estante_id)
    if tomo_id:
        asignaciones = asignaciones.filter(tomo__id=tomo_id)

    estantes = NivelEstante.objects.all()
    tomos = Tomo.objects.all()

    asignaciones_data = []
    for a in asignaciones:
        asignaciones_data.append({
            'id': a.id,
            'fecha_asignacion': a.fecha_asignacion.strftime("%Y-%m-%d"),
            'hora_asigancion': a.hora_asigancion.strftime("%H:%M:%S"),
            'estado_tomo': a.estado_tomo,
            'espacio_ocupado': a.espacio_ocupado,
            'estante': f"{a.estante_almacen.estante.nro_estante} - Nivel {a.estante_almacen.nivel.nro_nivel}",
            'tomo': f"{a.tomo.nro_tomo} - {a.tomo.titulo}",
            'url_edit': reverse('asignacion_tomo_update', args=[a.id]),
            'url_delete': reverse('asignacion_tomo_delete', args=[a.id]),
        })

    form = AsignacionTomoForm()

    return render(request, 'asignaciones_tomo/asignacion_tomo_list.html', {
        'asignaciones': asignaciones,
        'asignaciones_data': asignaciones_data,
        'form': form,
        'estantes': estantes,
        'tomos': tomos,
        'action_url': reverse('asignacion_tomo_create'),  # 👈 como en Tomos
        'title': 'Nueva Asignación de Tomo',
    })


def asignacion_tomo_create(request):
    if request.method == 'POST':
        form = AsignacionTomoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignación creada correctamente ✅")
            return redirect('inventario_tomos')
    else:
        form = AsignacionTomoForm()
    return render(request, 'asignaciones_tomo/asignacion_tomo_form.html', {
        'form': form,
        'title': 'Nueva Asignación de Tomo',
        'action_url': reverse('asignacion_tomo_create')
    })


def asignacion_tomo_update(request, pk):
    asignacion = get_object_or_404(AsignacionTomo, pk=pk)
    if request.method == 'POST':
        form = AsignacionTomoForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignación actualizada correctamente ✏️")
            return redirect('inventario_tomos')
    else:
        form = AsignacionTomoForm(instance=asignacion)

    return render(request, 'asignaciones_tomo/asignacion_tomo_form.html', {
        'form': form,
        'title': f'Editar Asignación #{asignacion.id}',
        'action_url': reverse('asignacion_tomo_update', args=[pk])
    })


def asignacion_tomo_delete(request, pk):
    asignacion = get_object_or_404(AsignacionTomo, pk=pk)
    asignacion.delete()
    messages.success(request, "Asignación eliminada correctamente 🗑️")
    return redirect('inventario_tomos')

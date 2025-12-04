from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect

from solicitudes.models import SolicitudMaterial, DetalleSolicitudMaterial
from personal.models import Personal


@login_required
def solicitudes_pendientes_view(request):
    """Solicitudes dirigidas a este jefe."""
    try:
        personal = Personal.objects.get(usuario=request.user)
    except Personal.DoesNotExist:
        messages.error(request, "No existe personal asignado a este usuario.")
        return render(request, "solicitudes/pendientes.html", {"solicitudes": []})

    solicitudes = SolicitudMaterial.objects.filter(
        dirigido_a=personal,
        estado_solicitud="pendiente"
    ).order_by("codigo_solicitud")

    return render(request, "solicitudes/pendientes.html", {
        "solicitudes": solicitudes
    })


@login_required
def atender_solicitud_view(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMaterial, pk=solicitud_id)

    try:
        personal = Personal.objects.get(usuario=request.user)
    except Personal.DoesNotExist:
        messages.error(request, "No existe personal asignado a este usuario.")
        return redirect('solicitudes:pending')

    if solicitud.dirigido_a != personal:
        messages.error(request, "No tienes permiso para atender esta solicitud.")
        return redirect('solicitudes:pending')

    if solicitud.estado_solicitud != 'pendiente':
        messages.warning(request, "Esta solicitud ya ha sido atendida.")
        return redirect('solicitudes:pending')

    detalles = DetalleSolicitudMaterial.objects.filter(solicitud=solicitud)

    return render(request, "solicitudes/atender.html", {
        "solicitud": solicitud,
        "detalles": detalles
    })


@login_required
def modificar_detalle_solicitud(request, detalle_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    detalle = get_object_or_404(DetalleSolicitudMaterial, pk=detalle_id)
    
    try:
        cantidad = int(request.POST.get("cantidad", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Cantidad inválida."}, status=400)

    if cantidad < 1:
        return JsonResponse({"error": "La cantidad debe ser al menos 1."}, status=400)

    if cantidad > detalle.material.cantidad_existente:
        return JsonResponse(
            {"error": f"Stock insuficiente. Disponible: {detalle.material.cantidad_existente}"},
            status=400
        )

    try:
        detalle.cantidad_solicitada = cantidad
        detalle.save()
        return JsonResponse({"ok": True, "nueva_cantidad": cantidad})
    except Exception as e:
        return JsonResponse({"error": "Error al actualizar la cantidad."}, status=500)


@login_required
def aprobar_solicitud(request, solicitud_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    solicitud = get_object_or_404(SolicitudMaterial, pk=solicitud_id)

    # Verificar permisos
    try:
        personal = Personal.objects.get(usuario=request.user)
        if solicitud.dirigido_a != personal:
            return JsonResponse({"error": "No tienes permiso para aprobar esta solicitud."}, status=403)
    except Personal.DoesNotExist:
        return JsonResponse({"error": "Usuario no válido."}, status=403)

    # Verificar que todos los detalles tengan stock suficiente
    detalles = DetalleSolicitudMaterial.objects.filter(solicitud=solicitud)
    for detalle in detalles:
        if detalle.cantidad_solicitada > detalle.material.cantidad_existente:
            return JsonResponse({
                "error": f"Stock insuficiente para {detalle.material.descripcion}. Disponible: {detalle.material.cantidad_existente}"
            }, status=400)

    try:
        with transaction.atomic():
            solicitud.estado_solicitud = "aprobada"
            solicitud.save()
            
            # Aquí podrías agregar lógica adicional como descontar del stock
            # for detalle in detalles:
            #     detalle.material.cantidad_existente -= detalle.cantidad_solicitada
            #     detalle.material.save()
            
        return JsonResponse({"ok": True, "msg": "Solicitud aprobada correctamente."})
    except Exception as e:
        return JsonResponse({"error": "Error al aprobar la solicitud."}, status=500)


@login_required
def rechazar_solicitud(request, solicitud_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    solicitud = get_object_or_404(SolicitudMaterial, pk=solicitud_id)

    # Verificar permisos
    try:
        personal = Personal.objects.get(usuario=request.user)
        if solicitud.dirigido_a != personal:
            return JsonResponse({"error": "No tienes permiso para rechazar esta solicitud."}, status=403)
    except Personal.DoesNotExist:
        return JsonResponse({"error": "Usuario no válido."}, status=403)

    try:
        solicitud.estado_solicitud = "rechazada"
        solicitud.save()
        return JsonResponse({"ok": True, "msg": "Solicitud rechazada correctamente."})
    except Exception as e:
        return JsonResponse({"error": "Error al rechazar la solicitud."}, status=500)
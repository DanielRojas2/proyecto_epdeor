from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from solicitudes.models import SolicitudMaterial, DetalleSolicitudMaterial
from solicitudes.models.EntregaMaterialSolicitado import EntregaMaterialSolicitado
from materiales.models.Material import Material

@login_required
def solicitudes_aprobadas_view(request):
    """Lista todas las solicitudes aprobadas para entrega con información mejorada."""
    solicitudes = SolicitudMaterial.objects.filter(
        estado_solicitud="aprobada"
    ).select_related(
        'creado_por__personal',
        'dirigido_a'
    ).prefetch_related(
        'detallesolicitudmaterial_set__material'
    ).order_by("fecha_solicitud", "hora_solicitud")
    
    # Agregar información de disponibilidad
    for solicitud in solicitudes:
        solicitud.total_materiales = solicitud.detallesolicitudmaterial_set.count()
        solicitud.puede_entregarse = True
        
        for detalle in solicitud.detallesolicitudmaterial_set.all():
            disponible = Material.objects.filter(
                descripcion=detalle.material,
                cantidad_existente__gt=0
            ).aggregate(total=Sum('cantidad_existente'))['total'] or 0
            
            if disponible < detalle.cantidad_solicitada:
                solicitud.puede_entregarse = False
                break
    
    return render(request, "solicitudes/entregas.html", {"solicitudes": solicitudes})

@login_required
def entregar_material_view(request, solicitud_id):
    """Vista mejorada para mostrar el formulario de entrega."""
    solicitud = get_object_or_404(
        SolicitudMaterial.objects.select_related(
            'creado_por__personal',
            'dirigido_a'
        ), 
        pk=solicitud_id
    )

    if solicitud.estado_solicitud != "aprobada":
        messages.error(request, "La solicitud no está aprobada para entrega.")
        return redirect('solicitudes:entregas_pendientes')

    solicitante = solicitud.creado_por.personal
    detalles = solicitud.detallesolicitudmaterial_set.select_related('material').all()
    
    entregas = []
    materiales_sin_stock = []
    
    for detalle in detalles:
        # Obtener materiales disponibles ordenados por fecha (FIFO)
        disponibles = Material.objects.filter(
            descripcion=detalle.material,
            cantidad_existente__gt=0
        ).order_by("creado")
        
        total_disponible = sum(a.cantidad_existente for a in disponibles)
        
        # Verificar si hay suficiente stock
        tiene_stock_suficiente = total_disponible >= detalle.cantidad_solicitada
        
        if not tiene_stock_suficiente:
            materiales_sin_stock.append({
                'material': detalle.material.descripcion,
                'solicitado': detalle.cantidad_solicitada,
                'disponible': total_disponible
            })
        
        entregas.append({
            "detalle": detalle,
            "disponibles": disponibles,
            "total_disponible": total_disponible,
            "tiene_stock_suficiente": tiene_stock_suficiente,
            "max_entregable": min(detalle.cantidad_solicitada, total_disponible)
        })

    return render(request, "solicitudes/entregar.html", {
        "solicitud": solicitud,
        "solicitante": solicitante,
        "entregas": entregas,
        "materiales_sin_stock": materiales_sin_stock,
        "puede_entregar": len(materiales_sin_stock) == 0
    })

@login_required
@transaction.atomic
def registrar_entrega(request, solicitud_id):
    """Vista mejorada para registrar la entrega con validaciones."""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    solicitud = get_object_or_404(SolicitudMaterial, pk=solicitud_id)
    
    if solicitud.estado_solicitud != "aprobada":
        return JsonResponse({
            "error": "La solicitud no está aprobada para entrega."
        }, status=400)

    detalles = solicitud.detallesolicitudmaterial_set.select_related('material').all()
    
    try:
        # Procesar datos del formulario
        data = {}
        for key, value in request.POST.items():
            if key.startswith("cantidad_"):
                detalle_id = key.replace("cantidad_", "")
                try:
                    cantidad = int(value)
                    if cantidad < 0:
                        raise ValueError("La cantidad no puede ser negativa")
                    data[detalle_id] = cantidad
                except ValueError as e:
                    return JsonResponse({
                        "error": f"Cantidad inválida para el detalle {detalle_id}: {str(e)}"
                    }, status=400)

        # Validar y procesar cada detalle
        for detalle in detalles:
            cantidad = data.get(str(detalle.id), 0)
            
            if cantidad == 0:
                continue  # Saltar materiales con cantidad 0
                
            if cantidad > detalle.cantidad_solicitada:
                return JsonResponse({
                    "error": f"La cantidad a entregar de {detalle.material.descripcion} excede lo solicitado"
                }, status=400)

            # Obtener asignaciones disponibles (FIFO)
            asignaciones = Material.objects.filter(
                descripcion=detalle.material,
                cantidad_existente__gt=0
            ).order_by("creado")
            
            restante = cantidad
            entregas_realizadas = []
            
            for asignacion in asignaciones:
                if restante <= 0:
                    break
                    
                entregar = min(asignacion.cantidad_existente, restante)
                
                # Crear registro de entrega
                entrega = EntregaMaterialSolicitado.objects.create(
                    cantidad_entregada=entregar,
                    solicitud=solicitud,
                    material_entregado=asignacion,
                    entregado_por=request.user,
                    fecha_entrega=timezone.now()
                )
                entregas_realizadas.append(entrega)
                
                # Actualizar stock del material
                asignacion.cantidad_existente -= entregar
                asignacion.save()
                
                # Actualizar cantidad existente del material
                material_principal = asignacion.descripcion
                material_principal.cantidad_existente = Material.objects.filter(
                    descripcion=material_principal,
                    cantidad_existente__gt=0
                ).aggregate(total=Sum('cantidad_existente'))['total'] or 0
                material_principal.save()
                
                restante -= entregar

            if restante > 0:
                # Revertir las entregas realizadas para este material
                for entrega in entregas_realizadas:
                    entrega.material_entregado.cantidad_existente += entrega.cantidad_entregada
                    entrega.material_entregado.save()
                EntregaMaterialSolicitado.objects.filter(id__in=[e.id for e in entregas_realizadas]).delete()
                
                return JsonResponse({
                    "error": f"No hay stock suficiente para {detalle.material.descripcion}. Solicitado: {cantidad}, Disponible: {cantidad - restante}"
                }, status=400)

        # Marcar solicitud como finalizada
        solicitud.estado_solicitud = "finalizada"
        solicitud.save()

        return JsonResponse({
            "success": True, 
            "message": "Entrega registrada correctamente. La solicitud ha sido finalizada.",
            "redirect_url": "/solicitudes/entregas/"  # URL para redirección
        })

    except Exception as e:
        transaction.set_rollback(True)
        return JsonResponse({
            "error": f"Error al procesar la entrega: {str(e)}"
        }, status=500)
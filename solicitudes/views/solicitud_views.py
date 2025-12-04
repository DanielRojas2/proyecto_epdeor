from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.urls import reverse

from materiales.models.Material import Material
from ..models import SolicitudMaterial, DetalleSolicitudMaterial
from personal.models import Personal

CARRITO_KEY = "carrito_materiales"

def _get_carrito(session):
    return session.get(CARRITO_KEY, {})

def _save_carrito(session, carrito):
    session[CARRITO_KEY] = carrito
    session.modified = True

@login_required
def solicitar_material_view(request):
    materiales = Material.objects.select_related('partida').filter(cantidad_existente__gte=1)
    return render(request, "solicitudes/solicitar_material.html", {"materiales": materiales})

@login_required
def carrito_parcial_view(request):
    carrito = _get_carrito(request.session)
    items = []
    for mid, qty in carrito.items():
        try:
            mat = Material.objects.get(pk=int(mid))
        except Material.DoesNotExist:
            continue
        items.append({"material": mat, "cantidad": qty})
    html = render_to_string("solicitudes/partials/carrito.html", {"items": items}, request=request)
    return JsonResponse({"html": html})

@login_required
def agregar_al_carrito(request, material_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")
    material = get_object_or_404(Material, pk=material_id)
    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Cantidad inválida"}, status=400)
    if cantidad < 1:
        return JsonResponse({"error": "La cantidad debe ser al menos 1"}, status=400)
    if cantidad > material.cantidad_existente:
        return JsonResponse({"error": f"Stock insuficiente. Disponible: {material.cantidad_existente}"}, status=400)

    carrito = _get_carrito(request.session)
    key = str(material.id)
    prev = int(carrito.get(key, 0))
    nuevo = prev + cantidad
    if nuevo > material.cantidad_existente:
        nuevo = material.cantidad_existente
    carrito[key] = nuevo
    _save_carrito(request.session, carrito)
    return JsonResponse({"ok": True, "carrito": carrito})

@login_required
def actualizar_carrito(request, material_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")
    material = get_object_or_404(Material, pk=material_id)
    try:
        cantidad = int(request.POST.get("cantidad", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Cantidad inválida"}, status=400)
    carrito = _get_carrito(request.session)
    key = str(material.id)
    if cantidad <= 0:
        carrito.pop(key, None)
    else:
        if cantidad > material.cantidad_existente:
            return JsonResponse({"error": f"Stock insuficiente. Disponible: {material.cantidad_existente}"}, status=400)
        carrito[key] = cantidad
    _save_carrito(request.session, carrito)
    return JsonResponse({"ok": True, "carrito": carrito})

@login_required
def eliminar_del_carrito(request, material_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")
    carrito = _get_carrito(request.session)
    carrito.pop(str(material_id), None)
    _save_carrito(request.session, carrito)
    return JsonResponse({"ok": True, "carrito": carrito})

@login_required
def generar_solicitud(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    carrito = _get_carrito(request.session)
    if not carrito:
        return JsonResponse({"error": "El carrito está vacío."}, status=400)

    try:
        personal = Personal.objects.get(usuario=request.user)
    except Personal.DoesNotExist:
        return JsonResponse({"error": "No existe registro de Personal para el usuario."}, status=400)

    jefe_personal = None
    if personal.cargo and personal.cargo.departamento and personal.cargo.departamento.jefe:
        jefe_personal = personal.cargo.departamento.jefe  # instancia Personal

    fecha_str = timezone.localdate().strftime("%d/%m/%Y")
    unidad_nombre = str(personal.cargo.unidad) if getattr(personal, "cargo", None) and getattr(personal.cargo, "unidad", None) else "Área"
    tipo_material_ref = request.POST.get("ref_tipo", "material de escritorio")

    cuerpo = (f"Solicito {tipo_material_ref}, para el Área {unidad_nombre}, dependiente de la {personal.cargo.departamento if personal.cargo else ''}, "
             f"ya que el material de escritorio coadyuva al cumplimento de responsabilidades que corresponden al Área {unidad_nombre}. Con la misma, adjunto SABS-1.")

    nota = (
        f"A: {jefe_personal.nombre if jefe_personal else '---'} {jefe_personal.apellido_paterno if jefe_personal else ''} {jefe_personal.apellido_materno if jefe_personal else ''}\n"
        f"De: {personal.nombre} {personal.apellido_paterno} {personal.apellido_materno or ''}\n"
        f"Ref: Solicitud de {tipo_material_ref} para el área de {unidad_nombre}\n"
        f"Fecha: {fecha_str}\n\n"
        f"{cuerpo}"
    )

    with transaction.atomic():
        # Guardamos la solicitud con la nota en 'observación'
        solicitud = SolicitudMaterial(
            creado_por=request.user,
            dirigido_a=jefe_personal,
            observación=nota  # <-- guarda la nota interna
        )
        solicitud.save()

        detalles = []
        for mid, qty in carrito.items():
            mat = get_object_or_404(Material, pk=int(mid))
            qty_int = int(qty)
            if qty_int <= 0:
                transaction.set_rollback(True)
                return JsonResponse({"error": f"Cantidad inválida para {mat.descripcion}"}, status=400)
            if qty_int > mat.cantidad_existente:
                transaction.set_rollback(True)
                return JsonResponse({"error": f"Stock insuficiente para {mat.descripcion}. Disponible: {mat.cantidad_existente}"}, status=400)

            # 2) RESERVAR: descontar del stock disponible
            mat.cantidad_existente -= qty_int
            mat.save()

            detalle = DetalleSolicitudMaterial(
                solicitud=solicitud,
                material=mat,
                cantidad_solicitada=qty_int
            )
            detalles.append(detalle)

        DetalleSolicitudMaterial.objects.bulk_create(detalles)

    # Limpiamos carrito
    _save_carrito(request.session, {})

    # Enviar correo (igual que antes)
    mail_sent = False
    if jefe_personal and getattr(jefe_personal, "usuario", None) and jefe_personal.usuario.email:
        try:
            subject = f"Solicitud {solicitud.codigo_solicitud} - Nueva solicitud de material"
            message = f"Se ha generado la solicitud {solicitud.codigo_solicitud} por {personal.nombre} {personal.apellido_paterno}.\n\nNota:\n{nota}\n\nPor favor revise el sistema."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [jefe_personal.usuario.email], fail_silently=True)
            mail_sent = True
        except Exception:
            mail_sent = False

    # 3) URLs de PDFs
    nota_pdf_url = reverse("solicitudes:nota_pdf", args=[solicitud.id])
    detalle_pdf_url = reverse("solicitudes:detalle_pdf", args=[solicitud.id])

    redirect_url = reverse("inicio:inicio")

    return JsonResponse({
        "ok": True,
        "msg": "Solicitud creada correctamente.",
        "solicitud_id": solicitud.id,
        "codigo": solicitud.codigo_solicitud,
        "nota": nota,
        "notificado_email": mail_sent,
        "nota_pdf_url": nota_pdf_url,
        "detalle_pdf_url": detalle_pdf_url,
        "redirect_url": redirect_url,
    })
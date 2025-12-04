from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..decorators import role_required
from ..models.Personal import Personal
from ..models.Cargo import Cargo
from ..forms import PersonalForm

@login_required
@role_required("sisadmin")
def usuarios(request):
    personal = Personal.objects.all()
    cargos = Cargo.objects.all()

    form = PersonalForm()

    if request.method == 'POST':
        personal_id = request.POST.get('personal_id')

        if personal_id:  
            instance = get_object_or_404(Personal, id=personal_id)
            form = PersonalForm(request.POST, instance=instance)
            operacion = "actualizado"

        else:
            form = PersonalForm(request.POST)
            operacion = "registrado"

        if form.is_valid():
            form.save()
            messages.success(request, f"Personal {operacion} correctamente.")
            return redirect('usuarios')

    return render(request, 'usuarios/usuarios.html', {
        'personal_form': form,
        'personal': personal,
        'cargos': cargos,
    })

@login_required
@role_required("sisadmin")
def toggle_estado_usuario(request, id):
    persona = get_object_or_404(Personal, id=id)

    persona.estado = "inactivo" if persona.estado == "activo" else "activo"
    persona.save()

    messages.info(request, "El estado del usuario fue actualizado")
    return redirect('usuarios')

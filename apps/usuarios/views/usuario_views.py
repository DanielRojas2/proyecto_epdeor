from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from ..models.Personal import Personal
from ..models.Cargo import Cargo
from ..forms.PersonalForm import PersonalForm

def usuario_list(request):
    usuarios = Personal.objects.all()
    cargos = Cargo.objects.all()
    return render(
        request, 'usuarios_index.html',
        {
            'usuarios':usuarios,
            'cargos': cargos,
        }
    )


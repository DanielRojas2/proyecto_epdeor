from django.shortcuts import render
from ..models.Personal import Personal

def usuario_list(request):
    usuarios = Personal.objects.all()
    return render(request, 'usuarios_index.html', {'usuarios':usuarios})

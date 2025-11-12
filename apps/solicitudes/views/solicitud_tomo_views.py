from django.shortcuts import render

def solicitar_tomo(request):
    return render(request, 'solicitud_tomo/solicitud_tomo.html')

import os

def get_upload_to(instance, filename):

    tomo = instance.tomo.titulo
    gestion = instance.tomo.gestion
    mes = instance.tomo.mes

    return os.path.join('archivos', gestion, mes, tomo, filename)

import os

def get_upload_to(instance, filename):

    tomo = instance.tomo.titulo

    return os.path.join('archivos', tomo, filename)

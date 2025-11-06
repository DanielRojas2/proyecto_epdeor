import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models.Unidad import Unidad

class Command(BaseCommand):
    help = "Poblar la tabla Unidad desde un archivo JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "archivo", nargs="?", type=str,
            help="Ruta al archivo JSON con unidades (opcional)"
        )

    def handle(self, *args, **options):
        archivo = options["archivo"]

        if not archivo:
            archivo = os.path.join(settings.BASE_DIR, "usuarios", "fixtures", "unidades.json")

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error al abrir JSON {archivo}: {e}"))
            return

        objetos = [Unidad(unidad=item["unidad"]) for item in data if "unidad" in item]

        Unidad.objects.bulk_create(objetos, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Se cargaron {len(objetos)} unidades."))
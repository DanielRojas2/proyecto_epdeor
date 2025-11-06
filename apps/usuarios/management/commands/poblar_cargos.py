import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models.Cargo import Cargo
from ...models.Departamento import Departamento
from ...models.Unidad import Unidad
from ...models.Rol import Rol
from django.db import transaction

class Command(BaseCommand):
    help = "Poblar la tabla Cargo desde un archivo JSON, vinculando Departamentos, Unidades y Roles"

    def add_arguments(self, parser):
        parser.add_argument(
            "archivo", nargs="?", type=str,
            help="Ruta al archivo JSON con cargos (opcional)"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        archivo = options["archivo"]

        if not archivo:
            archivo = os.path.join(
                settings.BASE_DIR,
                "usuarios",
                "fixtures",
                "cargos.json"
            )

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error al abrir JSON {archivo}: {e}")
            )
            return

        creados, ignorados = 0, 0

        for item in data:
            try:
                # Buscar las FK
                departamento = Departamento.objects.get(departamento=item["departamento"])
                unidad = Unidad.objects.get(unidad=item["unidad"])
                rol = Rol.objects.get(rol=item["rol"])

                # Crear cargo si no existe
                obj, creado = Cargo.objects.get_or_create(
                    cargo=item["cargo"],
                    departamento=departamento,
                    unidad=unidad,
                    rol=rol
                )
                if creado:
                    creados += 1
                else:
                    ignorados += 1

            except Departamento.DoesNotExist:
                self.stderr.write(
                    self.style.WARNING(f"Departamento no encontrado: {item['departamento']}")
                )
                ignorados += 1
            except Unidad.DoesNotExist:
                self.stderr.write(
                    self.style.WARNING(f"Unidad no encontrada: {item['unidad']}")
                )
                ignorados += 1
            except Rol.DoesNotExist:
                self.stderr.write(
                    self.style.WARNING(f"Rol no encontrado: {item['rol']}")
                )
                ignorados += 1
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error al crear cargo {item.get('cargo', '?')}: {e}")
                )
                ignorados += 1

        self.stdout.write(
            self.style.SUCCESS(f"Cargos creados: {creados}, ignorados: {ignorados}")
        )
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
        from django.db import connection
        connection.ensure_connection()
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
            self.stderr.write(self.style.ERROR(f"Error al abrir JSON {archivo}: {e}"))
            return

        creados, ignorados = 0, 0

        for item in data:
            try:
                # Buscar FKs
                departamento = Departamento.objects.get(departamento=item["departamento"])
                unidad = Unidad.objects.get(unidad=item["unidad"])

                # --- Crear Cargo sin roles (ManyToMany NO se asigna en get_or_create) ---
                cargo_obj, created = Cargo.objects.get_or_create(
                    cargo=item["cargo"],
                    departamento=departamento,
                    unidad=unidad
                )

                # Obtener lista de roles (si es string, convertirla en lista)
                roles_raw = item["rol"]
                if isinstance(roles_raw, str):
                    roles_raw = [roles_raw]

                # Buscar los roles
                roles_objs = []
                for rol_name in roles_raw:
                    try:
                        rol_obj = Rol.objects.get(rol=rol_name)
                        roles_objs.append(rol_obj)
                    except Rol.DoesNotExist:
                        self.stderr.write(
                            self.style.WARNING(f"Rol no encontrado: {rol_name}")
                        )

                # Asignar roles al cargo
                cargo_obj.rol.set(roles_objs)

                if created:
                    creados += 1
                else:
                    ignorados += 1

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error al procesar cargo {item.get('cargo', '?')}: {e}")
                )
                ignorados += 1

        self.stdout.write(
            self.style.SUCCESS(f"Cargos creados: {creados}, ignorados: {ignorados}")
        )

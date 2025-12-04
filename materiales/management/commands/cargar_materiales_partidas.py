# materiales/management/commands/cargar_materiales_partidas.py

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from materiales.models.PartidaPresupuestaria import PartidaPresupuestaria
from materiales.models.Material import Material


class Command(BaseCommand):
    help = "Carga PartidasPresupuestarias y Materiales desde JSON simples."

    def add_arguments(self, parser):
        parser.add_argument(
            '--partidas',
            type=str,
            default='materiales/fixtures/partidas.json',
            help='Ruta al JSON de partidas (relativa a BASE_DIR o absoluta).'
        )
        parser.add_argument(
            '--materiales',
            type=str,
            default='materiales/fixtures/materiales.json',
            help='Ruta al JSON de materiales (relativa a BASE_DIR o absoluta).'
        )
        parser.add_argument(
            '--reset-materiales',
            action='store_true',
            help='Borra todos los materiales antes de cargarlos de nuevo.'
        )

    def _resolver_ruta(self, ruta_str: str) -> Path:
        """Devuelve una ruta absoluta a partir de BASE_DIR si es relativa."""
        ruta = Path(ruta_str)
        if not ruta.is_absolute():
            ruta = Path(settings.BASE_DIR) / ruta
        if not ruta.exists():
            raise CommandError(f'No se encontró el archivo: {ruta}')
        return ruta

    @transaction.atomic
    def handle(self, *args, **options):
        # Resolver rutas
        ruta_partidas = self._resolver_ruta(options['partidas'])
        ruta_materiales = self._resolver_ruta(options['materiales'])

        self.stdout.write(self.style.MIGRATE_HEADING('==> Cargando partidas desde JSON'))
        with ruta_partidas.open('r', encoding='utf-8') as f:
            partidas_data = json.load(f)

        # Mapa índice -> instancia de Partida,
        # para poder usar el "partida": 8 de tu JSON de materiales
        indice_a_partida = {}

        for idx, item in enumerate(partidas_data, start=1):
            partida_num = item.get('partida')
            categoria = item.get('categoria')

            if not partida_num or not categoria:
                raise CommandError(
                    f'Registro de partida inválido (índice {idx}): {item}'
                )

            obj, created = PartidaPresupuestaria.objects.get_or_create(
                partida=partida_num,
                categoria=categoria,
            )

            indice_a_partida[idx] = obj

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [+] Partida creada: {obj.partida} - {obj.categoria}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'  [=] Partida ya existía: {obj.partida} - {obj.categoria}'
                    )
                )

        self.stdout.write(self.style.MIGRATE_HEADING('==> Cargando materiales desde JSON'))

        if options['reset_materiales']:
            borrados, _ = Material.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'  [!] Materiales borrados antes de la carga: {borrados}')
            )

        with ruta_materiales.open('r', encoding='utf-8') as f:
            materiales_data = json.load(f)

        for idx, item in enumerate(materiales_data, start=1):
            descripcion = item.get('descripcion')
            if not descripcion:
                raise CommandError(
                    f'Registro de material inválido (índice {idx}), falta descripción: {item}'
                )

            # En tu JSON de materiales, "partida": 8 hace referencia
            # al índice de la partida en partidas.json (8 = "39500 - Útiles de Escritorio")
            partida_ref = item.get('partida')
            partida_obj = None

            if isinstance(partida_ref, int):
                partida_obj = indice_a_partida.get(partida_ref)
                if not partida_obj:
                    raise CommandError(
                        f'No se encontró partida para índice {partida_ref} '
                        f'(material índice {idx}, descripción "{descripcion}")'
                    )
            else:
                # Si algún día usas directamente el código de partida en el JSON de materiales
                # (por ejemplo "39500"), también lo soportamos
                partida_obj = PartidaPresupuestaria.objects.filter(
                    partida=str(partida_ref)
                ).first()
                if not partida_obj:
                    raise CommandError(
                        f'No se encontró partida con código "{partida_ref}" '
                        f'(material índice {idx}, descripción "{descripcion}")'
                    )

            defaults = {
                'codigo_material': item.get('codigo_material') or '',
                'cantidad_minima': item.get('cantidad_minima', 1),
                'cantidad_existente': item.get('cantidad_existente', 0),
                'unidad_ingreso': item.get('unidad_ingreso', ''),
                'cantidad_x_unidad_ingreso': item.get('cantidad_x_unidad_ingreso', 1),
                'volumen': item.get('volumen', 'N/A'),
                'unidad_salida': item.get('unidad_salida', ''),
                'tipo_material': item.get('tipo_material', ''),
                'partida': partida_obj,
            }

            # Usamos get_or_create por descripción (que ya es unique en el modelo)
            material, created = Material.objects.get_or_create(
                descripcion=descripcion,
                defaults=defaults
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [+] Material creado: {material.descripcion} '
                        f'(código generado: {material.codigo_material})'
                    )
                )
            else:
                # Si ya existía, opcionalmente podrías actualizar sus campos:
                # for campo, valor in defaults.items():
                #     setattr(material, campo, valor)
                # material.save()
                self.stdout.write(
                    self.style.WARNING(
                        f'  [=] Material ya existía: {material.descripcion}'
                    )
                )

        self.stdout.write(self.style.SUCCESS('==> Carga completada correctamente ✅'))

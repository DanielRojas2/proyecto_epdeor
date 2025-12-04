from django.contrib import admin
from .models.Departamento import Departamento
from .models.Unidad import Unidad
from .models.Rol import Rol
from .models.Cargo import Cargo
from .models.Personal import Personal

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'creado', 'actualizado')
    search_fields = ('departamento',)
    ordering = ('departamento',)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('unidad', 'creado', 'actualizado')
    search_fields = ('unidad',)
    ordering = ('unidad',)

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'departamento', 'unidad', 'creado', 'actualizado')
    search_fields = ('cargo', 'departamento__departamento', 'unidad__unidad')
    list_filter = ('departamento', 'unidad')
    ordering = ('cargo',)

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'ci',
        'cargo',
        'estado',
        'alta',
        'baja',
        'usuario',
    )
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'ci', 'cargo__cargo')
    list_filter = ('estado', 'cargo__departamento', 'cargo__unidad')
    ordering = ('apellido_paterno', 'nombre')
    readonly_fields = ('usuario', 'alta')

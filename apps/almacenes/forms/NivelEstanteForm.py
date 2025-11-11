from django import forms
from ..models.NivelEstante import NivelEstante
from ..models.Nivel import Nivel

class NivelEstanteForm(forms.ModelForm):
    class Meta:
        model = NivelEstante
        fields = ['nivel', 'espacio_disponible']
        widgets = {
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'espacio_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'nivel': 'Nivel',
            'espacio_disponible': 'Espacio disponible (%)',
        }

    def __init__(self, *args, **kwargs):
        estante = kwargs.pop('estante', None)
        super().__init__(*args, **kwargs)
        if estante:
            niveles_usados = estante.nivelestante_set.values_list('nivel_id', flat=True)
            self.fields['nivel'].queryset = Nivel.objects.exclude(id__in=niveles_usados)

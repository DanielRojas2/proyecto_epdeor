from django import forms
from ..models.Estante import Estante

class EstanteForm(forms.ModelForm):
    class Meta:
        model = Estante
        fields = ['nro_estante']
        widgets = {
            'nro_estante': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'nro_estante': 'Número de Estante',
        }

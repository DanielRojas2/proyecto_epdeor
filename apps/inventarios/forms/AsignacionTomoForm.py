from django import forms
from ..models.AsignacionTomo import AsignacionTomo

class AsignacionTomoForm(forms.ModelForm):
    class Meta:
        model = AsignacionTomo
        fields = ['espacio_ocupado', 'estante_almacen', 'tomo']
        widgets = {
            'espacio_ocupado': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'estante_almacen': forms.Select(attrs={'class': 'form-control'}),
            'tomo': forms.Select(attrs={'class': 'form-control'}),
        }

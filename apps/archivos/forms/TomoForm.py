from django import forms
from ..models.Tomo import Tomo

class TomoForm(forms.ModelForm):
    class Meta:
        model = Tomo
        fields = ['nro_tomo', 'titulo', 'glosa', 'fecha_apertura']
        widgets = {
            'nro_tomo': forms.NumberInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'glosa': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_apertura': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

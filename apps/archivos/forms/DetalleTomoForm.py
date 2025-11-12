from django import forms
from ..models.DetalleTomo import DetalleTomo

class DetalleTomoForm(forms.ModelForm):
    class Meta:
        model = DetalleTomo
        fields = ['nombre_archivo', 'archivo']
        widgets = {
            'nombre_archivo': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

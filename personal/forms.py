from django import forms
from .models.Personal import Personal

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'ci', 'baja', 'cargo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'baja': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }

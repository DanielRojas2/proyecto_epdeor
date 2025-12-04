from django import forms
from .models import DetalleSolicitudMaterial

class DetalleCarritoForm(forms.ModelForm):
    class Meta:
        model = DetalleSolicitudMaterial
        fields = ['material', 'cantidad_solicitada']

    def clean_cantidad_solicitada(self):
        cantidad = self.cleaned_data.get('cantidad_solicitada')
        material = self.cleaned_data.get('material')
        if cantidad is None:
            raise forms.ValidationError("Cantidad requerida.")
        if cantidad < 1:
            raise forms.ValidationError("La cantidad debe ser al menos 1.")
        if material and cantidad > material.cantidad_existente:
            raise forms.ValidationError(f"No puede solicitar más de {material.cantidad_existente} unidades.")
        return cantidad

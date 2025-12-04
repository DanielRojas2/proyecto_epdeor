from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'lf--input',
            'placeholder': 'Nombre de Usuario'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'lf--input',
            'placeholder': 'Contraseña'
        })

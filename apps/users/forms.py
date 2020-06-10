from django import forms
from django.db import models
from .models import Delegacion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DelegacionForm(forms.ModelForm):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    def __init__(self, *args, **kwargs):
        super(DelegacionForm, self).__init__(*args, **kwargs)
        # no solo clases cualquier otro atributo se puede
        self.fields['nombre'].widget.attrs.update({'class':'form-control', 'placeholder':'Nombre'})

    class Meta:
        model = Delegacion
        fields = [
            'nombre',
        ]

class CreateEmplooyeeForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'username': 'Numero de empleado',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Institucional',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }   
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: 12345','required':True}),
            'first_name': forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Por ejemplo: Cesar Ernesto','required':True}),
            'last_name': forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Por ejemplo: Salazar Buelna','required':True}),
            'email': forms.EmailInput(attrs={'pattern':'[a-z0-9._-]+@([a-z0-9_-]+\.)*(uson\.|unison\.|staus\.)([a-z0-9_-]+\.)*[a-z]{2,4}$','class':'form-control','placeholder':'Por ejemplo: abcdef@mat.uson.mx','required':True}),
            #'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Por ejemplo: abcdef@mat.uson.mx','required':True}),
            'password1': forms.PasswordInput(attrs={'class':'form-control','placeholder':''}),
            'password2': forms.PasswordInput(attrs={'class':'form-control','placeholder':''}),
        }
    
class LoginEmplooyeeForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginEmplooyeeForm, self).__init__(*args, **kwargs)
        # no solo clases cualquier otro atributo se puede
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Número de empleado'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':''})

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        labels = {
            'username': 'Numero de empleado',
            'password': 'Contraseña',
        }
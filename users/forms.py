from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import *
# Extendemos del original


class UsuarioCreateForm(UserCreationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto
    email = forms.EmailField(label="Correo electrónico")
    nombres = forms.CharField(label='Nombres')
    apellidos = forms.CharField(label='Apellidos')

    class Meta:
        model = Usuario
        fields = ["email", "nombres", "apellidos", "password1", "password2"]


class UsuarioFormEdit(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email','nombres','apellidos','is_active','is_staff', 'is_superuser', 'is_client')

        labels = {
            'email':'Correo Electrónico',
            'nombres':'Nombres',
            'apellidos':'Apellidos',
            'is_active':'Cuenta Activa',
            'is_staff':'Funcionario',
            'is_superuser':'Administrador',
            'is_client':'Cliente',
            }
        widgets= {
            'email': forms.TextInput(attrs={'class':'form-control','id':'email','readonly':True}),
            'nombres': forms.TextInput(attrs={'class':'form-control','id':'nombres'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control','id':'apellidos'}),
            'is_active':forms.CheckboxInput(attrs={'class':'form-control','id':'is_active'}),
            'is_staff':forms.CheckboxInput(attrs={'class':'form-control','id':'is_staff'}),
            'is_superuser':forms.CheckboxInput(attrs={'class':'form-control','id':'is_superuser'}),
            'is_client':forms.CheckboxInput(attrs={'class':'form-control','id':'is_client'}),
        }

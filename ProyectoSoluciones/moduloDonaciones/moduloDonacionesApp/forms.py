from django import forms
from .models import UserModel , DonModel

#Formulario Usuarios
class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'

    #Validación ingreso de correo para que no se caiga
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['idU'].required = True
        self.fields['nombre'].required = True
        self.fields['correo'].required = True
        self.fields['correo'].error_messages = {
            'required': 'Este campo es obligatorio',
            'invalid': 'Correo inválido. Debe ingresar uno real'}
        self.fields['nombre'].error_messages = {
            'required': 'Este campo es obligatorio'
        }

#Formulario Donaciones
class DonForm(forms.ModelForm):
    class Meta:
        model = DonModel
        fields = '__all__'

    #validación que en caso no se ingrese detalle, no haya problema
    

"""{
  "rules": {
    ".read": "now < 1699758000000",  // 2023-11-12
    ".write": "now < 1699758000000",  // 2023-11-12
  }
}"""
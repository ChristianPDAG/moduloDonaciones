from django import forms
from .models import UserModel , DonModel

#Formulario Usuarios
class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'

    #Validación ingreso de correo para que no se caiga
    def clean_email(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')

        if correo and '@' not in correo:
            raise forms.ValidationError("El correo debe contener @")
        return correo
    
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
from django import forms
from .models import UserModel

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'

    def clean_email(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get('correo')

        if correo and '@' not in correo:
            raise forms.ValidationError("El correo debe contener @")
        return cleaned_data

#class UserForm(forms.Form):
 #   id = forms.IntegerField()
  #  nombre = forms.CharField(max_length=50)
   # correo = forms.CharField(max_length=50)

    """
    idU= forms.IntegerField()
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    """
   
"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idU'].widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['correo'].widget.attrs['class'] = 'form-control'
        """
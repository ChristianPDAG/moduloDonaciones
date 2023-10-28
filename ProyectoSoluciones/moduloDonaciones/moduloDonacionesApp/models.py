from django.db import models

# Create your models here.

#Modelo formulario usuarios
class UserModel(models.Model):

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    fono = models.CharField(max_length=100)


   # ids.widget.attrs['class'] = ' form-control'
  #  nombre.widget.attrs['class'] = ' form-control'
   # correo.widget.attrs['class'] = ' form-control'

#Modelo formulario donaciones
class DonModel(models.Model):
    tipo_prenda = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    talla = models.CharField(max_length=100)
    detalle = models.CharField(max_length=100, null="True")
    img = models.ImageField(blank="True", null="True")


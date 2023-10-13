from django.db import models

# Create your models here.

class UserModel(models.Model):

    idU= models.IntegerField()
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()

   # ids.widget.attrs['class'] = ' form-control'
  #  nombre.widget.attrs['class'] = ' form-control'
   # correo.widget.attrs['class'] = ' form-control'
  
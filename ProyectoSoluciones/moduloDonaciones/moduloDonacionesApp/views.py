from django.shortcuts import render ,redirect

from django.apps import apps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from .forms import UserForm
from django import forms

def connectDB():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../modulodonaciones-firebase-adminsdk-zvcs8-3e5c71d008.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://modulodonaciones-default-rtdb.firebaseio.com" #Your database URL
        })
    dbconn = db.reference("Data")
    return dbconn

#class FormUs(View):
#    template_name = 'template/form_donacion.html'
 #   cred = credentials.Certificate('./modulodonaciones-firebase-adminsdk-zvcs8-3e5c71d008.json')
  #  firebase_admin.initialize_app(cred,{'databaseURL':'https://modulodonaciones-default-rtdb.firebaseio.com'})
   # ref = db.reference('data')
    #datos = ref.get()



# Create your views here.
def renderFormDon(request):
    return render(request,'template/form_donacion.html')



def renderFormUs(request):
    users = []
    dbconn = connectDB()
    tblUsers = dbconn.get()
    for key, value in tblUsers.items():
        users.append({"ID":value["ID"],"nombre":value["nombre"],"correo":value["correo"]})
    return render(request,'template/Form_Usuarios.html', {"users" : users})

"""
def renderUsForm(request):
    form = UserForm()
    return render(request,'template/Form_Usuarios.html',{'form': form})
"""
def addUs(request):
    error_message = None
    if request.method == 'GET':
        form = UserForm()
        return render(request,'template/form_usuario2.html', {'form' : form})
    if request.method == 'POST':
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                idU = form.cleaned_data.get("idU")
                nombre = form.cleaned_data.get("nombre")
                correo = form.cleaned_data.get("correo")

                dbconn = connectDB()
                dbconn.push({"ID":idU,"nombre": nombre,"correo":correo})
                return redirect('Form_Usuarios')
        
        except forms.ValidationError as e:
            print(f"ValidationError: {e}")
            form.add_error('correo',str(e))
            error_message = str(e)

    return render(request, 'template/form_usuario2.html', {'form': form, 'error_message': error_message})

        
    
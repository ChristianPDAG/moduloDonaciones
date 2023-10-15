from django.shortcuts import render ,redirect

from django.apps import apps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from .forms import UserForm , DonForm
from django import forms


#Conexión a base de datos firebase
def connectDB():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../modulodonaciones-firebase-adminsdk-zvcs8-3e5c71d008.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://modulodonaciones-default-rtdb.firebaseio.com" 
        })
    dbconn = db.reference("Data")
    return dbconn




#Listar usuarios en /formUsuario
def renderFormUs(request):
    users = []
    dbconn = connectDB()
    tblUsers = dbconn.get()
    for key, value in tblUsers.items():
        users.append({"ID":value["ID"],"nombre":value["nombre"],"correo":value["correo"]})
    return render(request,'template/Form_Usuarios.html', {"users" : users})


#Añadir usuario en /formUsuario2
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
                new_user = dbconn.push({"ID": idU, "nombre": nombre, "correo": correo, "donaciones": {}})
                
                return redirect('form_donaciones', user_id=new_user.key)
        
        except forms.ValidationError as e:
            print(f"ValidationError: {e}")
            form.add_error('correo',str(e))
            error_message = str(e)

    return render(request, 'template/form_usuario2.html', {'form': form, 'error_message': error_message})


#formulario de donación, se asocia al usuario añadido anteriormente
def addDon(request, user_id):
    if request.method == 'GET':
        form_don = DonForm()
        return render (request,'template/form_donacion.html',{'form': form_don })
    if request.method == 'POST':
        form_don = DonForm(request.POST)
        if form_don.is_valid():
            tipo_prenda = form_don.cleaned_data.get('tipo_prenda')
            estado = form_don.cleaned_data.get('estado')
            talla = form_don.cleaned_data.get('talla')
            detalle = form_don.cleaned_data.get('detalle')

            connectDB()
            user_ref = db.reference(f'Data/{user_id}')

            new_donation = user_ref.child('donaciones').push({"tipo_prenda":tipo_prenda,"estado":estado,"talla":talla,"detalle":detalle})
            return redirect('form_donaciones' ,user_id)


        else:
            form_don = DonForm()

        return render(request,'template/form_donacion.html',{'form_don':form_don})

    

        
    
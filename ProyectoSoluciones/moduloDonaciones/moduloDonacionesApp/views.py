from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps
import firebase_admin
from firebase_admin import credentials , storage
from firebase_admin import db
from .forms import UserForm 
from .forms import DonForm
from django import forms
from datetime import date , datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



#Render Navbar
def renderNavbar(request):
    return render(request, 'template/donaciones.html')

def renderHistorial(request, user_id):
    users = []
    db_ref = connectDB()
    user_data = db_ref.child(user_id).get()

    user_info = {
        "donaciones": user_data.get("donaciones", [])
        }

    users.append(user_info)

    return render(request, 'template/historial.html', {"users": users})

def renderHistorialGeneral(request):
    users = []
    db_ref = connectDB()
    tblUsers = db_ref.get()

    for key, value in tblUsers.items():
        user_info = {
            
            "donaciones": value.get("donaciones", [])
        }
    

    users.append(user_info)

    return render(request, 'template/historial_general.html', {"users": users})

#Conexión a base de datos firebase
def connectDB():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../modulodonaciones-firebase-adminsdk-zvcs8-3e5c71d008.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://modulodonaciones-default-rtdb.firebaseio.com",
            "storageBucket": "modulodonaciones.appspot.com"
        })

    dbconn = db.reference("Data")
    return dbconn 

#Listar usuarios en /formUsuario
@login_required
def renderFormUs(request):
    users = []
    db_ref = connectDB()

    tblUsers = db_ref.get()

    for key, value in tblUsers.items():
        user_info = {
            "id":key,
            "nombre": value.get("nombre"),
            "apellido": value.get("apellido"),
            "correo": value.get("correo"),
            "fono": value.get("fono"),
            "donaciones": value.get("donaciones", [])
        }

        users.append(user_info)

    return render(request, 'template/Form_Usuarios.html', {"users": users})
                  

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
                nombre = form.cleaned_data.get("nombre")
                apellido = form.cleaned_data.get("apellido")
                correo = form.cleaned_data.get("correo")
                fono = form.cleaned_data.get("fono")


                dbconn = connectDB()
                new_user = dbconn.push({"nombre": nombre,"apellido":apellido, "correo": correo,"fono":fono, "donaciones": {}})
                
                return redirect('form_donaciones', user_id=new_user.key)
        
        except forms.ValidationError as e:
            print(f"ValidationError: {e}")
            form.add_error('correo',str(e))
            error_message = str(e)

    return render(request, 'template/form_usuario2.html', {'form': form, 'error_message': error_message})



#formulario de donación, se asocia al usuario añadido anteriormente
def addDon(request, user_id):
    dt = datetime.now()
    ddtt = dt.strftime('%d-%m-%Y')
    if request.method == 'GET':
        form_don = DonForm()
        return render(request, 'template/form_donacion.html', {'form_don': form_don })

    if request.method == 'POST':
        form_don = DonForm(request.POST, request.FILES)

        if form_don.is_valid():
            tipo_prenda = form_don.cleaned_data.get('tipo_prenda')
            estado = form_don.cleaned_data.get('estado')
            talla = form_don.cleaned_data.get('talla')
            detalle = form_don.cleaned_data.get('detalle')
            img = form_don.cleaned_data.get('img')

            connectDB()

            #Subir la imagen a Firebase Storage
            if img:
                img_path = f'{user_id}_{tipo_prenda}_{estado}_{talla}_{detalle}.jpg'
                print(img_path)
                bucket = storage.bucket()
                blob = bucket.blob(img_path)
                try:
                    blob.upload_from_file(img, content_type='image/jpeg')
                except Exception as e:
                    print(f"Error al cargar el archivo en Firebase Storage: {e}")
            else:
                img_path = None


            #Convierte la ruta del archivo en la url de la imagen
            if img_path:
                img_url = f'https://firebasestorage.googleapis.com/v0/b/modulodonaciones.appspot.com/o/{img_path}?alt=media'
            else:
                img_url = None

            user_ref = db.reference(f'Data/{user_id}')

            # Crear la nueva donación
            new_donation = user_ref.child('donaciones').push({
                "tipo_prenda": tipo_prenda,
                "estado": estado,
                "talla": talla,
                "detalle": detalle,
                "img": img_url, # Almacena la ruta del archivo en Firebase Storage
                "estado": "En proceso",
                "fecha": ddtt  
            })

            return redirect('form_donaciones', user_id)
        else:
            return render(request, 'template/form_donacion.html', {'form_don': form_don})
        

    
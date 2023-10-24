from django.shortcuts import render ,redirect

from django.apps import apps
import firebase_admin
from firebase_admin import credentials , storage
from firebase_admin import db
from .forms import UserForm 
from .forms import DonForm
from django import forms


#Render Navbar
def renderNavbar(request):
    return render(request, 'template/donaciones.html')

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

def urlCreate():
    connectDB()
    blob = connectDB.bucket.blob('static/img/boton.png')
    download_url = blob.generate_signed_url()
    return(download_url)

#Listar usuarios en /formUsuario
def renderFormUs(request):
    users = []
    db_ref = connectDB()

    tblUsers = db_ref.get()

    for key, value in tblUsers.items():
        user_info = {
            "ID": value.get("ID"),
            "nombre": value.get("nombre"),
            "correo": value.get("correo"),
            "donaciones": value.get("donaciones", [])
        }

        users.append(user_info)

    return render(request, 'template/Form_Usuarios.html', {"users": users})
                  
"""    users = []
    donaciones = []
    db_ref = connectDB()
    
    tblUsers = dbconn.get()
  
    for key, value in tblUsers.items():
        users.append({"ID":value["ID"],
                      "nombre":value["nombre"],
                      "correo":value["correo"]})
        
    return render(request,'template/Form_Usuarios.html', {"users" : users})



    # Obtener datos de usuarios desde Firebase
    users_data = db_ref.child('usuarios').get()

    for user_key, user_value in users_data.items():
        user_info = {
            "ID": user_value.get("ID"),
            "nombre": user_value.get("nombre"),
            "correo": user_value.get("correo"),
        }

        # Agregar información de donaciones si está disponible
        donaciones_data = user_value.get("donaciones")
        if donaciones_data:
            user_info["donaciones"] = donaciones_data

        users.append(user_info)

    return render(request, 'template/Form_Usuarios.html', {"users": users})"""




"""dbconn = connectDB()
    tblUsers = dbconn.get()
  
    for key, value in tblUsers.items():
        users.append({"ID":value["ID"],"nombre":value["nombre"],"correo":value["correo"]})
    return render(request,'template/Form_Usuarios.html', {"users" : users})"""

""" for key, value in tblUsers.items():
        donaciones.append({"Talla":value["talla"],"tipo de prenda":value["tipo_prenda"],"Estado":value["estado"],"Detalle":value["detalle"]})  """  
    


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

            # Subir la imagen a Firebase Storage
            if img:
                img_path = f'{tipo_prenda}_{estado}_{talla}_{detalle}.jpg'
                print(img_path)
                bucket = storage.bucket()
                blob = bucket.blob(img_path)
                try:
                    blob.upload_from_file(img, content_type='image/jpeg')
                except Exception as e:
                    print(f"Error al cargar el archivo en Firebase Storage: {e}")
            else:
                img_path = None


            # Convierte la ruta del archivo en la URL de la imagen
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
                "img": img_path  # Almacena la ruta del archivo en Firebase Storage
            })

            return redirect('form_donaciones', user_id)
        else:
            # Manejar el caso donde el formulario no es válido
            return render(request, 'template/form_donacion.html', {'form_don': form_don})
        
"""
def addDon(request, user_id):
    if request.method == 'GET':
        form_don = DonForm()
        return render (request,'template/form_donacion.html',{'form': form_don })
    if request.method == 'POST':
        form_don = DonForm(request.POST, request.FILES)
        if form_don.is_valid():
            tipo_prenda = form_don.cleaned_data.get('tipo_prenda')
            estado = form_don.cleaned_data.get('estado')
            talla = form_don.cleaned_data.get('talla')
            detalle = form_don.cleaned_data.get('detalle')
            img = form_don.cleaned_data.get('img')
            img_url = storage.child(f'Data/{user_id}/donaciones/{new_donation.key}/img').get_url(None)

            connectDB()
            user_ref = db.reference(f'Data/{user_id}')

            new_donation = user_ref.child('donaciones').push({"tipo_prenda":tipo_prenda,"estado":estado,"talla":talla,"detalle":detalle,"img":img})
            return redirect('form_donaciones' ,user_id)


        else:
            form_don = DonForm()

        return render(request,'template/form_donacion.html',{'form_don':form_don})
"""
    

        
    
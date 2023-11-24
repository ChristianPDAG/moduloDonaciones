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
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.contrib.auth.decorators import user_passes_test

def is_special_user(user):
    return user.groups.filter(name='GODS').exists()

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

#Generar pdf
@login_required
def generate_pdf(request):
    user_id = request.user.id  # Obtén el ID del usuario 

    # Obtiene los datos de la variable de sesión
    general_donaciones = request.session.get('general_donaciones', [])

    # Crea la respuesta HTTP para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="historial.pdf"'

    # Crea un objeto PDF con ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define los estilos de la tabla
    styles = getSampleStyleSheet()
    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Crea la tabla de historial de donaciones
    data = [['Tipo de prenda', 'Talla', 'Estado', 'Detalle', 'Imagen', 'Estado Respuesta','Fecha']]
    for donation in general_donaciones:
        data.append([
            donation.get('tipo_prenda', 'Sin información'),
            donation.get('talla', 'Sin información'),
            donation.get('estado', 'Sin información'),
            donation.get('detalle', 'Sin información'),
            'Imagen solo en la web',  # Puedes agregar un enlace para abrir la imagen, si lo deseas
            donation.get('estadoR', 'Sin información'),
            donation.get('fecha', 'Sin información')
        ])

    table = Table(data)
    table.setStyle(style_table)

    elements.append(Paragraph(f"Historial de Donaciones", styles['Title']))
    elements.append(table)

    # Agrega una página en blanco (o salto de página) al final
    elements.append(PageBreak())

    # Construye el PDF
    doc.build(elements)

    return response

@user_passes_test(is_special_user, login_url='/admin/login/')
def renderHistorial(request, user_id):
    users = []
    db_ref = connectDB()
    user_data = db_ref.child(user_id).get()

    user_info = {
        "donaciones": user_data.get("donaciones", [])
        }

    users.append(user_info)

    return render(request, 'template/historial.html', {"user_id":user_id, "users": users})



#Listar todas las donaciones /historial_don, requiere estar logueado
@user_passes_test(is_special_user, login_url='/admin/login/')
def renderHistorialGeneral(request):
    general_donaciones = []
    db_ref = connectDB()
    tblUsers = db_ref.get()

    search_term = request.POST.get('search_term', '')  # Obtener el término de búsqueda desde la URL

    for key, value in tblUsers.items():
        user_donations = value.get("donaciones", [])
        for donation_id in user_donations:
            donation_data = user_donations[donation_id]
            
            # Obtiene valores
            tipo_prenda = donation_data.get("tipo_prenda", "")
            estado = donation_data.get("estado", "")
            talla = donation_data.get("talla", "")
            detalle = donation_data.get("detalle", "")
            estadoR = donation_data.get("estadoR", "")
            fecha = donation_data.get("fecha", "")

            # Realizar la búsqueda en los datos de donación
            if (search_term in tipo_prenda or
            search_term in estado or
            search_term in talla or
            search_term in detalle or
            search_term in estadoR or
            search_term in fecha):
                general_donaciones.append(donation_data)

                request.session['general_donaciones'] = general_donaciones

    return render(request, 'template/historial_general.html', {"donations": general_donaciones, "search_term": search_term})

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
                "estadoR": "En proceso",
                "fecha": ddtt  
            })

            ## AQUI QUIERO AGREGAR LA LOGICA PARA ACTUALIZAR EL "estadoR"

            return redirect('form_donaciones', user_id)
        else:
            return render(request, 'template/form_donacion.html', {'form_don': form_don})
        

    
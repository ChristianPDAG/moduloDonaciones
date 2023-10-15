import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../modulodonaciones-firebase-adminsdk-zvcs8-3e5c71d008.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://modulodonaciones-default-rtdb.firebaseio.com" #Your database URL
    })

dbref = db.reference("Data")
dbref.push( { "ID": 1, "nombre": "Toyota ", "correo": "toyota@mail","donaciones":[{"tipo_prenda":"Polera","estado":"Nuevo","talla":"L","detalle":"Jaja"}] } )
dbref.push( { "ID": 2, "nombre": " Camry", "correo": "camry@mail" } )



print(dbref.get())
dbref.get() 

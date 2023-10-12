from django.shortcuts import render

# Create your views here.
def renderFormDon(request):
    return render(request,'template/Form_Donacion.html')

def renderFormUs(request):
    return render (request,'template/Form_Usuarios')
"""moduloDonaciones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from moduloDonacionesApp.views import renderFormUs
from moduloDonacionesApp.views import addUs
from moduloDonacionesApp.views import addDon
from moduloDonacionesApp.views import renderNavbar , renderHistorial, renderHistorialGeneral, generate_pdf


urlpatterns = [
    path("admin/", admin.site.urls),
    path("formUsuario/", renderFormUs, name = 'Form_Usuarios'),
    path("formUsuario2/", addUs),
    path("formDonacion/<str:user_id>/", addDon, name = 'form_donaciones'),
    path("navbar/", renderNavbar),
    path("historial/<str:user_id>/",renderHistorial, name='ver_donaciones'),
    path("historial_don/", renderHistorialGeneral, name='historial_don'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),

]

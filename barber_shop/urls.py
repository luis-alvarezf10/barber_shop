from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Acceso al sitio de administración de Django
    path('admin/', admin.site.urls), 

    path('auth/', include('usuarios.urls')), 

    path('agenda/', include('agenda.urls')), 

    path('finanzas/', include('finanzas.urls')), 
]

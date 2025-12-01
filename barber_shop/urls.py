from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Acceso al sitio de administración de Django
    path('admin/', admin.site.urls), 

    path('auth/', include('Users.urls')), 

    path('agenda/', include('Schedule.urls')), 

    path('finanzas/', include('Finance.urls')), 
]

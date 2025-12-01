from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    return redirect('users:login')

urlpatterns = [
    path('', home, name='home'),
    
    # Acceso al sitio de administración de Django
    path('admin/', admin.site.urls), 

    path('auth/', include('users.urls')), 

    path('agenda/', include('schedule.urls')), 

    path('finanzas/', include('finance.urls')), 
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

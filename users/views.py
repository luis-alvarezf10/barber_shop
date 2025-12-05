from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, receptionist_or_admin, barber_only

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.name}!')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('users:login')

@login_required(login_url='users:login')
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
        'role': user.get_role_display(),
        'is_admin': user.is_admin,
        'is_barber': user.is_barber,
        'is_receptionist': user.is_receptionist,
    }
    return render(request, 'users/dashboard.html', context)


# Vista temporal para crear el primer superusuario en producción
# ELIMINAR DESPUÉS DE CREAR EL ADMIN
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import os

@csrf_exempt
def create_first_admin(request):
    from .models import User
    from django.db import connection
    from django.db.utils import OperationalError, ProgrammingError
    
    try:
        # Intentar verificar si las tablas existen
        try:
            user_count = User.objects.count()
        except (OperationalError, ProgrammingError) as e:
            # Las tablas no existen, ejecutar migraciones
            if 'does not exist' in str(e) or 'no such table' in str(e):
                try:
                    call_command('migrate', '--noinput')
                    return HttpResponse('''
                        <html>
                        <body style="font-family: Arial; padding: 50px; text-align: center;">
                            <h1>✅ Migraciones ejecutadas exitosamente</h1>
                            <p>Las tablas de la base de datos han sido creadas.</p>
                            <p><a href="/auth/setup-admin/" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Crear Administrador</a></p>
                        </body>
                        </html>
                    ''')
                except Exception as migrate_error:
                    return HttpResponse(f'Error ejecutando migraciones: {str(migrate_error)}', status=500)
            else:
                raise
        
        # Si llegamos aquí, las tablas existen
        if user_count > 0:
            return JsonResponse({
                'error': f'Ya existen {user_count} usuarios en el sistema. Esta vista está deshabilitada.'
            }, status=403)
        
        if request.method == 'POST':
            # Obtener credenciales desde el request
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            name = request.POST.get('name', 'Administrador').strip()
            
            if not username or not password or not email:
                return JsonResponse({
                    'error': 'Se requieren username, email y password'
                }, status=400)
            
            try:
                # Crear el superusuario
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    name=name,
                    last_name='',
                    phone_number='',
                    role='admin',
                    is_staff=True,
                    is_superuser=True
                )
                
                return JsonResponse({
                    'success': True,
                    'message': f'Superusuario {username} creado exitosamente',
                    'username': username,
                    'login_url': '/auth/login/'
                })
            except Exception as e:
                return JsonResponse({
                    'error': f'Error al crear usuario: {str(e)}'
                }, status=400)
        
        # Mostrar formulario simple
        return render(request, 'users/create_admin.html')
        
    except Exception as e:
        return HttpResponse(f'Error del servidor: {str(e)}', status=500)

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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def create_first_admin(request):
    # Solo permitir si no hay usuarios en la base de datos
    from .models import User
    
    if User.objects.exists():
        return JsonResponse({
            'error': 'Ya existen usuarios en el sistema. Esta vista está deshabilitada.'
        }, status=403)
    
    if request.method == 'POST':
        # Obtener credenciales desde variables de entorno o request
        username = request.POST.get('username') or os.environ.get('ADMIN_USERNAME', 'admin')
        email = request.POST.get('email') or os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = request.POST.get('password') or os.environ.get('ADMIN_PASSWORD')
        name = request.POST.get('name', 'Administrador')
        
        if not password:
            return JsonResponse({
                'error': 'Se requiere una contraseña'
            }, status=400)
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                name=name,
                role='admin'
            )
            return JsonResponse({
                'success': True,
                'message': f'Superusuario {username} creado exitosamente',
                'username': username
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=400)
    
    # Mostrar formulario simple
    return render(request, 'users/create_admin.html')

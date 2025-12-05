from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, receptionist_or_admin, barber_only

def login_view(request):
    # Solo redirigir si está autenticado Y es un GET request
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.name}!')
            # Usar next parameter si existe, sino dashboard
            next_url = request.GET.get('next', 'users:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('users:login')

@login_required(login_url='users:login')
def dashboard_view(request):
    try:
        user = request.user
        context = {
            'user': user,
            'role': user.get_role_display(),
            'is_admin': user.is_admin,
            'is_barber': user.is_barber,
            'is_receptionist': user.is_receptionist,
        }
        return render(request, 'users/dashboard.html', context)
    except Exception as e:
        messages.error(request, f'Error al cargar dashboard: {str(e)}')
        return redirect('users:login')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, receptionist_or_admin, barber_only

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Forzar que se guarde la sesión
            request.session.save()
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

@login_required(login_url='users:login')
def employees_view(request):
    from .models import User
    
    # Obtener el filtro del query parameter
    role_filter = request.GET.get('role', 'all')
    
    # Filtrar empleados según el rol seleccionado
    if role_filter == 'all':
        employees = User.objects.exclude(is_superuser=True).order_by('role', 'name')
    else:
        employees = User.objects.filter(role=role_filter).order_by('name')
    
    # Contar por rol
    total_admins = User.objects.filter(role='admin').count()
    total_barbers = User.objects.filter(role='barber').count()
    total_receptionists = User.objects.filter(role='receptionist').count()
    
    total_employees = User.objects.count()
    
    context = {
        'employees': employees,
        'role_filter': role_filter,
        'total_employees': total_employees,
        'total_admins': total_admins,
        'total_barbers': total_barbers,
        'total_receptionists': total_receptionists,
    }
    return render(request, 'users/employees.html', context)

@login_required(login_url='users:login')
@admin_required
def add_employee_view(request):
    from .models import User, ROLES_CHOICES
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            username = request.POST.get('username')
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            national_id = request.POST.get('national_id')
            address = request.POST.get('address')
            role = request.POST.get('role')
            password = request.POST.get('password')
            profile_image = request.FILES.get('profile_image')
            
            # Validaciones básicas
            if not all([username, name, last_name, email, phone_number, role, password]):
                messages.error(request, 'Por favor completa todos los campos obligatorios')
                return redirect('users:add_employee')
            
            # Verificar si el username ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe')
                return redirect('users:add_employee')
            
            # Verificar si el email ya existe
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado')
                return redirect('users:add_employee')
            
            # Verificar si la cédula ya existe (si se proporcionó)
            if national_id and User.objects.filter(national_id=national_id).exists():
                messages.error(request, 'La cédula ya está registrada')
                return redirect('users:add_employee')
            
            # Crear el nuevo empleado
            employee = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                name=name,
                last_name=last_name,
                phone_number=phone_number,
                national_id=national_id if national_id else None,
                address=address if address else None,
                role=role
            )
            
            # Agregar imagen de perfil si se proporcionó
            if profile_image:
                employee.profile_image = profile_image
                employee.save()
            
            messages.success(request, f'Empleado {name} {last_name} agregado exitosamente')
            return redirect('users:employees')
            
        except Exception as e:
            messages.error(request, f'Error al agregar empleado: {str(e)}')
            return redirect('users:add_employee')
    
    context = {
        'roles': ROLES_CHOICES,
    }
    return render(request, 'users/add_employee.html', context)


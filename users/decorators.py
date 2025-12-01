from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            
            if request.user.role in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes permisos para acceder a esta sección')
            return redirect('users:dashboard')
        return wrapper
    return decorator

def admin_required(view_func):
    return role_required('admin')(view_func)

def receptionist_or_admin(view_func):
    return role_required('admin', 'receptionist')(view_func)

def barber_only(view_func):
    return role_required('barber')(view_func)

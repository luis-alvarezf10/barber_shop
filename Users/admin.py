from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('name', 'last_name', 'email', 'national_id', 'phone_number', 'address', 'profile_image')}),
        ('Rol y Permisos', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'role', 'name', 'last_name', 'phone_number', 'profile_image'),
        }),
    )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'phone_number', 'national_id')
    search_fields = ('name', 'last_name', 'phone_number', 'national_id')
    list_filter = ('address',)

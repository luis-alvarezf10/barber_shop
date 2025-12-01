from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# Constantes para los roles de usuario
ROLES_CHOICES = (
    ('admin', 'Administrador'),
    ('barber', 'Barbero'),
    ('receptionist', 'Recepcionista'),
)

# Luigi: reestructurado el objeto user, ahora maneja autenticacion amo django <3
class User(AbstractUser):
    # Usamos UUID como clave primaria (Id) para todos los modelos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='users/profiles/', null=True, blank=True, verbose_name='Foto de Perfil')

    role = models.CharField(
        max_length=20,
        choices=ROLES_CHOICES,
        default='barber', # Rol por defecto
        verbose_name='users roles'
    ) 
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_receptionist(self):
        return self.role == 'receptionist'

    @property
    def is_barber(self):
        return self.role == 'barber'

    # Luigi: aquí deben definirse las acciones principales de aplicacion para cada usuario que usa el sistema, y esta es una buena manera de manejdar la validacion
    def has_module_perms(self, app_label):
        if self.is_superuser or self.is_admin:
            return True
        
        if self.is_receptionist:
            return app_label in ['users', 'schedule', 'finance']
        
        if self.is_barber:
            return app_label in ['schedule']
        
        return False

    def has_perm(self, perm, obj=None):
        # Luigi: aquí se definen los permisos principales
        if self.is_superuser or self.is_admin:
            return True
        

        # Luigi: Tema de permisos de recepcionista, pero como no he realizado el diseño no lo tengo claro. Tengo sueño mamañemas
        if self.is_receptionist:
            allowed_perms = [
                'users.view_client', 'users.add_client', 'users.change_client',
                'schedule.view_appointment', 'schedule.add_appointment', 'schedule.change_appointment',
                'schedule.view_services', 'schedule.view_barberservices',
                'finance.view_bill', 'finance.add_bill', 'finance.add_billservices', 'finance.add_billproduct',
                'finance.view_product', 'finance.view_billservices', 'finance.view_billproduct',
            ]
            return perm in allowed_perms
        
        # Luigi: permisos de barbero, el autocompletado hace maravillas
        if self.is_barber:
            
            allowed_perms = [
                'schedule.view_appointment',
                'schedule.view_services',
                'schedule.view_barberservices',
                'finance.view_billservices',  # Solo para ver sus comisiones
            ]
            return perm in allowed_perms
        
        return False 


# Luigi: Reestructurado los datos requeridos de cliente
class Client(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        
    def __str__(self):
        return f"{self.name} {self.last_name}"
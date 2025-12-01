from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# Constantes para los roles de usuario
ROLES_CHOICES = (
    ('admin', 'Administrador'),
    ('barber', 'Barbero'),
    ('receptionist', 'Recepcionista'),
)

class Users(AbstractUser):
    """
    Modelo de Usuario personalizado que incluye el campo 'rol'.
    Este modelo reemplaza el modelo User por defecto de Django.
    """
    # Usamos UUID como clave primaria (Id) para todos los modelos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    
    role = models.CharField(
        max_length=20,
        choices=ROLES_CHOICES,
        default='barber', # Rol por defecto
        verbose_name='Rol del Usuario'
    )
    
    # Campos adicionales para la información personal
    IDcedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return self.username
    
    # Es necesario definir los campos related_name para evitar conflictos con el modelo User por defecto
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_name="usuario_set", 
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="usuario_set", 
        related_query_name="usuario",
    )

class Client(models.Model):

    id_client = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    IDcedula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    phonenumber = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
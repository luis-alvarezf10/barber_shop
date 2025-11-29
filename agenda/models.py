from django.db import models
from usuarios.models import Usuario, Cliente
import uuid

class Servicio(models.Model):

    id_servicio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_servicio = models.CharField(max_length=100, unique=True)
    costo = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        
    def __str__(self):
        return self.nombre_servicio

class BarberoServicio(models.Model):

    # Filtramos para asegurar que solo se relacionen con usuarios con rol 'barber'
    barbero = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'barber'}, 
        verbose_name="Barbero"
    )
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="Servicio")
    
    class Meta:
        verbose_name = 'Habilidad del Barbero'
        verbose_name_plural = 'Habilidades de Barberos'
        unique_together = ('barbero', 'servicio') # Un barbero solo puede tener un servicio registrado a la vez
        
    def __str__(self):
        return f"{self.barbero.username} puede hacer {self.servicio.nombre_servicio}"

class Cita(models.Model):
    """
    Modelo para registrar las citas agendadas por la recepcionista.
    """
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    
    id_cita = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    # El barbero asignado para esta cita
    barbero = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, # Si el barbero se va, la cita no se borra
        null=True, 
        limit_choices_to={'rol': 'barber'}
    )
    
    fecha_hora = models.DateTimeField()
    duracion_minutos = models.IntegerField(default=30)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['fecha_hora']
        
    def __str__(self):
        return f"Cita de {self.cliente.nombre} con {self.barbero.username if self.barbero else 'No Asignado'} @ {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"
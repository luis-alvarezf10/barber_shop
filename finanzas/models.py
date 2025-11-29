from django.db import models
from usuarios.models import Cliente, Usuario
from agenda.models import Servicio
import uuid

# PRODUCTOS Y EGRESOS

class Producto(models.Model):
    id_producto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_producto = models.CharField(max_length=150)
    costo_compra = models.FloatField(default=0.0, verbose_name="Costo de Compra")
    precio_venta = models.FloatField(default=0.0, verbose_name="Precio de Venta al Cliente")

    def __str__(self):
        return self.nombre_producto

class Egreso(models.Model):

    RECURRENCIA_CHOICES = (
        ('unico', 'Único'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    razon = models.CharField(max_length=255)
    costo = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    tipo_recurrencia = models.CharField(max_length=10, choices=RECURRENCIA_CHOICES, default='unico')
    fecha_proximo_pago = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.razon} - ${self.costo}"


# FACTURACION 

class Factura(models.Model):
    id_factura = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    
    # La recepcionista que procesó la venta
    recepcionista = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'receptionist'}
    )
    
    monto_total = models.FloatField(default=0.0)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, default='Efectivo')
    
    def __str__(self):
        return f"Factura #{self.id_factura.hex[:8]} - Total: ${self.monto_total}"

class FacturaServicio(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True)
    
    # Barbero que realizó el servicio
    barbero = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'barber'}
    )
    
    costo_unitario = models.FloatField() # Precio de venta del servicio al momento de la venta
    cantidad = models.IntegerField(default=1)
    
    # Campos calculados y registrados para el dashboard del Barbero:
    porcentaje_comision = models.FloatField(default=0.0) # Porcentaje acordado
    monto_comision = models.FloatField(default=0.0)      # Monto que gana el Barbero !!!Ajustar porcentaje
    
    class Meta:
        verbose_name = 'Servicio Facturado'
        verbose_name_plural = 'Servicios Facturados'
        unique_together = ('factura', 'servicio', 'barbero') # Un barbero solo puede hacer mas de un servicio en una factura, pero se almacena por separado

class FacturaProducto(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    
    costo_unitario = models.FloatField() # Precio de venta del producto al momento de la venta
    cantidad = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = 'Producto Facturado'
        verbose_name_plural = 'Productos Facturados'
        unique_together = ('factura', 'producto')
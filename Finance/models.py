from django.db import models
from Users.models import Client, Users
from Schedule.models import Services
import uuid

# PRODUCTOS Y EGRESOS

class Product(models.Model):
    id_product = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=150)
    purchase_price = models.FloatField(default=0.0, verbose_name="Costo de Compra")
    selling_price = models.FloatField(default=0.0, verbose_name="Precio de Venta al Cliente")

    def __str__(self):
        return self.product_name

class Outflow(models.Model):

    RECURRENCIA_CHOICES = (
        ('unico', 'Único'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reazon = models.CharField(max_length=255)
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    frequency_date = models.CharField(max_length=10, choices=RECURRENCIA_CHOICES, default='unico')
    next_payment_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.reazon} - ${self.price}"


# FACTURACION 

class Bill(models.Model):
    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    
    # La recepcionista que procesó la venta
    recepcionist = models.ForeignKey(
        Users, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'receptionist'}
    )
    
    total_amount = models.FloatField(default=0.0)
    emision_date = models.DateTimeField(auto_now_add=True)
    paiment_method = models.CharField(max_length=50, default='Efectivo')
    
    def __str__(self):
        return f"Factura #{self.bill_id.hex[:8]} - Total: ${self.total_amount}"

class BillServices(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    
    # Barbero que realizó el servicio
    barber = models.ForeignKey(
        Users, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'barber'}
    )
    
    unitary_price = models.FloatField() # Precio de venta del servicio al momento de la venta
    quantity = models.IntegerField(default=1)
    
    # Campos calculados y registrados para el dashboard del Barbero:
    commission_percentage = models.FloatField(default=0.0) # Porcentaje acordado
    commission_ammount = models.FloatField(default=0.0)      # Monto que gana el Barbero !!!Ajustar porcentaje
    
    class Meta:
        verbose_name = 'Servicio Facturado'
        verbose_name_plural = 'Servicios Facturados'
        unique_together = ('bill', 'service', 'barber') # Un barbero solo puede hacer mas de un servicio en una factura, pero se almacena por separado

class BillProduct(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    unitary_price = models.FloatField() # Precio de venta del producto al momento de la venta
    quantity = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = 'Producto Facturado'
        verbose_name_plural = 'Productos Facturados'
        unique_together = ('bill', 'product')
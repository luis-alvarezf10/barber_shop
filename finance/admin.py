from django.contrib import admin
from .models import Product, Outflow, Bill, BillServices, BillProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'purchase_price', 'selling_price')
    search_fields = ('product_name',)

@admin.register(Outflow)
class OutflowAdmin(admin.ModelAdmin):
    list_display = ('reazon', 'price', 'date', 'frequency_date', 'next_payment_date')
    list_filter = ('frequency_date', 'date')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'client', 'recepcionist', 'total_amount', 'emision_date', 'paiment_method')
    list_filter = ('emision_date', 'paiment_method')
    search_fields = ('client__name',)

@admin.register(BillServices)
class BillServicesAdmin(admin.ModelAdmin):
    list_display = ('bill', 'service', 'barbero', 'unitary_price', 'quantity', 'commission_ammount')
    list_filter = ('barbero',)

@admin.register(BillProduct)
class BillProductAdmin(admin.ModelAdmin):
    list_display = ('bill', 'product', 'unitary_price', 'quantity')
    search_fields = ('product__product_name',)

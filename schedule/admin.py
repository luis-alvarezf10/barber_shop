from django.contrib import admin
from .models import Services, BarberServices, Appointment

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'price')
    search_fields = ('service_name',)

@admin.register(BarberServices)
class BarberServicesAdmin(admin.ModelAdmin):
    list_display = ('barber', 'service')
    list_filter = ('barber',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'barber', 'time_hour', 'status', 'duration_minutes')
    list_filter = ('status', 'barber', 'time_hour')
    search_fields = ('client__name',)

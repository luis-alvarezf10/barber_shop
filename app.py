import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

# Ejecutar migraciones automáticamente en el primer request
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError

try:
    # Verificar si las tablas existen
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM django_migrations LIMIT 1")
except OperationalError:
    # Si no existen, ejecutar migraciones
    print("Ejecutando migraciones...")
    call_command('migrate', '--noinput')
    print("Migraciones completadas!")

from application.wsgi import application

# Vercel necesita que la aplicación se llame 'app'
app = application

#!/bin/bash
# Instala dependencias
pip install -r requirements.txt

# Ejecuta migraciones
python manage.py migrate --noinput

# Recolecta archivos estáticos
python manage.py collectstatic --noinput --clear
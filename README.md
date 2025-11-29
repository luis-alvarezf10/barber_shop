La app 'agenda' es para manejar citas, horarios y la relacion entre Barberos y servicios.

La app 'finanzas' es para manejar ingresos, gastos, productos, comisiones y reportes financieros del negocio.

La app 'usuarios' es para manejar la autenticación y perfiles de usuarios, incluyendo el manejo de los barberos y clientes.

PASOS PARA CREAR LA BASE DE DATOS Y PARA CONFIGURAR EL PROGRAMA CORRECTAMENTE

1. Crear el entorno virtual en el directorio raiz.
    python -m venv .venv

2. Hacer el git clone
    git clone <repo_url>

3. Instalar las dependencias
    pip install -r requirements.txt

4. Hacer la migración y aplicarla.
    python manage.py makemigrations
    python manage.py migrate

5. Crear un super usuario
    python manage.py createsuperuser

LISTO NO LA CAGUEN  

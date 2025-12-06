import os
from pathlib import Path
from dotenv import load_dotenv

# Luis: Configuración de rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Luis: Cargar variables de entorno desde archivo .env para desarrollo local
load_dotenv(BASE_DIR / '.env')

# Luis: Asegurar que BASE_DIR sea siempre un objeto Path
if isinstance(BASE_DIR, str):
    BASE_DIR = Path(BASE_DIR)


# Luis: Configuración de seguridad y debug
# DEBUG debe ser False en producción, True en desarrollo
DEBUG = os.environ.get('DEBUG', 'True') == 'True' 

# Luis: SECRET_KEY es obligatoria en producción, tiene valor por defecto en desarrollo
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345') 
if not DEBUG and SECRET_KEY == 'dev-secret-key-change-in-production-12345':
    raise Exception("ERROR DE SEGURIDAD: SECRET_KEY no está configurada en producción.")

# Luis: ALLOWED_HOSTS define qué dominios pueden acceder a la aplicación
allowed_hosts_string = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,.vercel.app')
ALLOWED_HOSTS = allowed_hosts_string.split(',')

# Luis: Aplicaciones instaladas en el proyecto

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Luis: Apps personalizadas del proyecto
    'schedule',
    'finance',
    'users',
]

# Luis: Modelo de usuario personalizado en lugar del User por defecto de Django
AUTH_USER_MODEL = 'users.User'

# Luis: Middleware - orden importa, WhiteNoise debe ir después de SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Luis: Para servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Luis: Archivo principal de URLs
ROOT_URLCONF = 'application.urls'

# Luis: Configuración de templates (plantillas HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Luis: Carpeta global de templates
        'APP_DIRS': True,  # Luis: Buscar templates dentro de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Luis: Aplicación WSGI para deployment
WSGI_APPLICATION = 'application.wsgi.application'


# Luis: Configuración de base de datos
# Si existe DATABASE_URL o POSTGRES_URL, usa PostgreSQL (Neon)
# Si no, usa SQLite para desarrollo local
DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')

if DATABASE_URL:
    # Luis: Producción/Testing - PostgreSQL (Neon)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,  # Luis: Mantener conexión abierta por 10 minutos
            conn_health_checks=True,  # Luis: Verificar salud de la conexión
        )
    }
else:
    # Luis: Desarrollo local - SQLite (si no hay DATABASE_URL en .env)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Luis: Validadores de contraseñas para seguridad
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Luis: Configuración de internacionalización
LANGUAGE_CODE = 'en-us'

# Luis: Zona horaria de Venezuela
TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True


# Luis: Configuración de archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'

# Luis: Carpeta donde Django buscará archivos estáticos durante desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Luis: Carpeta donde se recopilarán todos los archivos estáticos en producción
# Se ejecuta con: python manage.py collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Luis: Archivos subidos por usuarios (fotos de perfil, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Luis: Configuración de almacenamiento para Vercel con WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",  # Luis: Comprime archivos estáticos
    },
}

# Luis: Tipo de clave primaria por defecto para modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Luis: Configuración de sesiones para mantener usuarios logueados
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Luis: Guardar sesiones en base de datos
SESSION_COOKIE_SECURE = not DEBUG  # Luis: True en producción (HTTPS), False en desarrollo
SESSION_COOKIE_HTTPONLY = True  # Luis: No accesible desde JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # Luis: Protección contra CSRF
SESSION_COOKIE_AGE = 1209600  # Luis: 2 semanas de duración
SESSION_SAVE_EVERY_REQUEST = True  # Luis: Guardar sesión en cada request para evitar loops
CSRF_COOKIE_SECURE = not DEBUG  # Luis: True en producción (HTTPS), False en desarrollo
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False

# Luis: Dominios confiables para CSRF en producción (Vercel)
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
        'https://nex-barber-shop.vercel.app',
    ]

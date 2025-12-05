import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Asegurar que BASE_DIR sea siempre un objeto Path
if isinstance(BASE_DIR, str):
    BASE_DIR = Path(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = os.environ.get('DEBUG') == 'True' 

SECRET_KEY = os.environ.get('SECRET_KEY') 
if not SECRET_KEY:
    raise Exception("ERROR DE SEGURIDAD: SECRET_KEY no está configurada en Vercel.")


allowed_hosts_string = os.environ.get('ALLOWED_HOSTS', '.vercel.app')
ALLOWED_HOSTS = allowed_hosts_string.split(',')
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', #authentication
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #apps
    'schedule',
    'finance',
    'users',
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Usar PostgreSQL en producción, SQLite en desarrollo
DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')

if DATABASE_URL:
    # Producción: usar PostgreSQL desde variable de entorno
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desarrollo: usar SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

# Carpeta donde Django buscará archivos estáticos durante desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Carpeta donde se recopilarán todos los archivos estáticos en producción (python manage.py collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (archivos subidos por usuarios)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración para Vercel - servir archivos estáticos con WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de sesiones para Vercel
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SECURE = not DEBUG  # True en producción
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1209600  # 2 semanas
SESSION_SAVE_EVERY_REQUEST = True  # Guardar sesión en cada request
CSRF_COOKIE_SECURE = not DEBUG  # True en producción
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Permitir acceso desde JavaScript si es necesario

# Configurar CSRF_TRUSTED_ORIGINS para Vercel
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
        'https://nex-barber-shop.vercel.app',
    ]

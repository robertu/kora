from datetime import timedelta
from pathlib import Path
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2rmxim9bjb)1+9eoaj0i@9ho02h8dt2fx6!pq8jptyqg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['kora.1kb.pl',]
CSRF_TRUSTED_ORIGINS = ['https://kora.1kb.pl']
API_V1_STR: str = "/api/v1"

AUTH_USER_MODEL = "user.User"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',

    # Third party
    'corsheaders',
    
    # Custom Apps
    "app.blog",
    "app.user",
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOT_DIR / 'db.sqlite3',
    }
}


DATABASES = {'default': env.db("DATABASE_URL", default="sqlite:////app/app.db")}
DATABASES['default']["ATOMIC_REQUESTS"] = True

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Static files
STATIC_URL = "/s/"
STATICFILES_DIRS = [BASE_DIR / "static", ]
STATIC_ROOT = ROOT_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files 
MEDIA_URL = "/media/"
MEDIA_ROOT = ROOT_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PROJECT_NAME = "kora"

###### Custom settings ######
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'your.email.host'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'your email host user'
# EMAIL_HOST_PASSWORD = 'your email host password'
# LOGIN_URL = 'http://127.0.0.1:3000'  # reverse_lazy('user:login')
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_URL = 'user:logout'
# LOGOUT_REDIRECT_URL = 'home'
# SIGNUP_REDIRECT_URL = 'user:email_verification_sent'


CORS_ALLOWED_ORIGINS = [
    "https://kora.1kb.pl",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)


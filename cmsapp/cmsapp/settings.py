from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where collected static files will be stored
# Media files (Uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Secret key and debug settings
SECRET_KEY = "django-insecure-5s1@5jgz(uqw-zw!8)azmw$7txa2o=ty3s0tz#wo&m3kd8+*9+"
DEBUG = True
ALLOWED_HOSTS = []

GRAPPELLI_ADMIN_TITLE = "EMININ STUDENT CMS"
GRAPPELLI_AUTOCOMPLETE_LIMIT = 10
GRAPPELLI_SWITCH_USER = True

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "drf_yasg",
    "djoser",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_extensions",
    "storages",
    "ckeditor",
    "ckeditor_uploader",
    "debug_toolbar",
    "django_celery_beat",
    "django_celery_results",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "channels",
    "grappelli.dashboard",
    "grappelli",  # Grappelli should be included
    "accounts",
    "content",
    "courses",
    'enrollments',  
    "assessments",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Add this line
]

ROOT_URLCONF = "cmsapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Directory where global templates are stored
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "cmsapp.wsgi.application"
ASGI_APPLICATION = "cmsapp.asgi.application"  # For Django Channels

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# CORS Headers configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Crispy Forms configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django AllAuth configuration
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1  # Required for Django AllAuth

# Celery configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"

# CKEditor configuration
CKEDITOR_UPLOAD_PATH = "uploads/"

# Django Debug Toolbar configuration
INTERNAL_IPS = ["127.0.0.1"]

# Channels configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cms',
        'USER': 'root',
        'PASSWORD': '1001',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', default_storage_engine=INNODB",  # Change this line
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
        'TIME_ZONE': 'UTC',
    }
}


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


CKEDITOR_CONFIGS = {
    'default': {
        'versionCheck': False
    }
}

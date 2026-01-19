from pathlib import Path
import os
from dotenv import load_dotenv
import sys

load_dotenv()

import logging
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR / 'api'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'

if PRODUCTION:
    DEBUG = False
    
    DOMAIN_NAME = 'rms-labs.ru'
    
    ALLOWED_HOSTS = [
        DOMAIN_NAME,
        f'www.{DOMAIN_NAME}',
        'localhost',
        '127.0.0.1',
        'backend',
        'nginx',
    ]
    
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    
    CORS_ALLOWED_ORIGINS = [
        f"https://{DOMAIN_NAME}",
        f"https://www.{DOMAIN_NAME}",
    ]
    
    CSRF_TRUSTED_ORIGINS = [
        f"https://{DOMAIN_NAME}",
        f"https://www.{DOMAIN_NAME}",
    ]
    
else:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        'backend',
        'nginx',
        'frontend',
        '192.168.1.106',
        '0.0.0.0',
        '*',
    ]
    
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://192.168.1.106:3000",
        "http://192.168.1.106:4173", 
        "http://192.168.1.106:80",
    ]

    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173", 
        "http://localhost:4173",
        "http://192.168.1.106:3000",
        "http://192.168.1.106:4173",
        "http://192.168.1.106:80",
    ]

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'AUTH_COOKIE_ACCESS': 'access_token',
    'AUTH_COOKIE_REFRESH': 'refresh_token',
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_MAX_AGE': 60 * 60 * 24 * 7,
}

if PRODUCTION:
    SIMPLE_JWT['AUTH_COOKIE_SECURE'] = True
    SIMPLE_JWT['AUTH_COOKIE_SAMESITE'] = 'None'
else:
    SIMPLE_JWT['AUTH_COOKIE_SECURE'] = False
    SIMPLE_JWT['AUTH_COOKIE_SAMESITE'] = 'Lax'

if os.getenv('DOCKERIZED', 'False').lower() == 'true':
    CORS_ALLOWED_ORIGINS.extend([
        "http://frontend:3000",
        "http://frontend:4173",
        "http://nginx:80",
    ])
    CSRF_TRUSTED_ORIGINS.extend([
        "http://frontend:3000", 
        "http://frontend:4173",
        "http://nginx:80",
    ])

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    'api',
    'employees',
    'documentation',
    'research',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.RequestLoggingMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'secret_lab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'secret_lab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'secret_lab'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Для сбора статики
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Дополнительные папки со статикой

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.auth_logging.AuditedJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Разрешения по умолчанию
    # ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3000/hour',
        'user': '10000/hour',
        'auth': '50/hour',
        'api': '10000/hour',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'RETRY_ON_TIMEOUT': True,
            'MAX_CONNECTIONS': 40,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'KEY_PREFIX': 'secret_lab',
        'TIMEOUT': 60 * 15,
    }
}

REDIS_CONFIG = {
    'maxmemory': '500mb',
    'maxmemory-policy': 'allkeys-lru',
    'maxmemory-samples': 5,
    'save': '900 1 300 10 60 10000',
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'secret_lab'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '{asctime} | {levelname:8} | {name} | {module}:{funcName}:{lineno} | {message}',
            'style': '{',
        },
        'json': {
            '()': 'api.log_formatters.AuditLogFormatter',
        },
    },
    
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'json_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'stream': sys.stdout,
        },
        'file_app': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter': 'json',
            'encoding': 'utf-8',
        },
        'file_errors': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter': 'json',
            'encoding': 'utf-8',
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'json',
            'encoding': 'utf-8',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'json_console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins', 'json_console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security', 'mail_admins', 'json_console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_app', 'json_console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'json_console', 'file_app'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'api.auth': {
            'handlers': ['console', 'json_console', 'file_security'],
            'level': 'INFO',
            'propagate': False,
        },
        'api.data': {
            'handlers': ['console', 'json_console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'api.security': {
            'handlers': ['file_security', 'json_console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'employees': {
            'handlers': ['console', 'json_console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'documentation': {
            'handlers': ['console', 'json_console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'research': {
            'handlers': ['console', 'json_console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'audit': {
            'handlers': ['file_security', 'json_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

import os
os.makedirs('logs', exist_ok=True)

try:
    logger.info("Настройки приложения загружены успешно", 
                extra={'debug_mode': DEBUG, 'allowed_hosts': ALLOWED_HOSTS})
except Exception as e:
    print(f"Ошибка при инициализации логирования: {e}")

logger.info(f"DEBUG mode: {DEBUG}")
logger.info(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
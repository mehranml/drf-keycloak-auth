""" Settings config for the drf_keycloak_auth application """
import os

from django.conf import settings
from rest_framework.settings import APISettings
from django.core.management.utils import get_random_secret_key

from drf_keycloak_auth.settings import DEFAULTS, USER_SETTINGS

# DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = 'testapp.CustomUser'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(' ')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'testapp',
    'rest_framework',
    'drf_keycloak_auth',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles'
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdatabase',
    }
}
DEBUG = True

ROOT_URLCONF = 'testapp.urls'

SECRET_KEY = get_random_secret_key()

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'drf_keycloak_auth.authentication.KeycloakAuthentication',
        # 'drf_keycloak_auth.authentication.KeycloakMultiAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ]
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
)

# Django Logging Information
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'drf_keycloak_auth': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        # 'urllib3': {
        #     'handlers': ['console'],
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        #     'propagate': True,
        # },
        # 'requests_oauthlib': {
        #     'handlers': ['console'],
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        #     'propagate': True,
        # }
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'drf_keycloak_auth.middleware.AuthSessionMiddleware',
]

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)

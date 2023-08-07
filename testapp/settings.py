""" Settings config for the drf_keycloak_auth application """
import datetime
import os

from django.conf import settings
from rest_framework.settings import APISettings
from django.core.management.utils import get_random_secret_key

import json

from drf_keycloak_auth.settings import DEFAULTS, USER_SETTINGS

# DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = 'testapp.CustomUser'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(' ')

INSTALLED_APPS = [
    'testapp',
    'drf_keycloak_auth',
    'django.contrib.auth',
    'django.contrib.contenttypes'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdatabase',
    }
}
DEBUG = True

ROOT_URLCONF = 'testapp.urls'

SECRET_KEY = get_random_secret_key()

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
        }
    },
}

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)

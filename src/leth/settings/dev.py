from .base import *

DEBUG = True

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'PORT': 5432
            }
        }

PROJECT_APPS += [
        'django-debug-toolbar',
        ]

# Celery settings
BROKER_URL = 'amqp://guest:guest@rabbit//'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

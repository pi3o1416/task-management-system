
from .base import *

ALLOWED_HOSTS = ['tms.monirhossain.dev', '103.174.51.237']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PROD_DB_NAME'),
        'USER': env('PROD_DB_USER'),
        'PASSWORD': env('PROD_DB_PASS'),
        'HOST': env('PROD_DB_HOST'),
        'PORT': env('PROD_DB_PORT')
    }
}


from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DEV_DB_NAME'),
        'USER': env('DEV_DB_USER'),
        'PASSWORD': env('DEV_DB_PASS'),
        'HOST': env('DEV_DB_HOST'),
        'PORT': env('DEV_DB_PORT')
    }
}

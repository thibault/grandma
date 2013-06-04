from base import *

from django.core.exceptions import ImproperlyConfigured

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "grandma",
        "USER": "grandma",
        "PASSWORD": "grandma",
        "HOST": "localhost",
        "PORT": "",
    },
}

ALLOWED_HOSTS = []

try:
    from prod_private import *
except ImportError:
    raise ImproperlyConfigured('Create a prod_private.py file with production config variables')

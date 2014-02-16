from base import *  # noqa

from django.core.exceptions import ImproperlyConfigured


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "grandma",
        "USER": "grandma",
        "PASSWORD": "grandma",
        "HOST": "localhost",
        "PORT": "",
    },
}

INSTALLED_APPS += (
    'south',
    'raven.contrib.django.raven_compat',
    'gunicorn',
)

ALLOWED_HOSTS = ['.dontforgetgrandma.com']

LOGGING['handlers'].update({
    'sentry': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'raven.contrib.django.handlers.SentryHandler',
    }})
LOGGING['loggers']['']['handlers'] = ['console', 'syslog', 'mail_admins', 'sentry']

try:
    from prod_private import *  # noqa
except ImportError:
    raise ImproperlyConfigured('Create a prod_private.py file with production config variables')

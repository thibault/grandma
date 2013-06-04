from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

INSTALLED_APPS += (
    'debug_toolbar',
    'casper',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/grandma.mail'
DEFAULT_FROM_EMAIL = 'django@grandma'
MAILING_CAMPAIGN_HEADER = 'X-Mailjet-Campaign'

NEXMO_API = 'http://rest.nexmo.com/sms/json'
NEXMO_USERNAME = 'username'
NEXMO_PASSWORD = 'password'
NEXMO_FROM='Grandma'

PAYMILL_PUBLIC_KEY = '17525186687258c77db2ac5ba2a940d6'
PAYMILL_PRIVATE_KEY = 'cd3ddf7e028d1a8790b6605022153074'
PAYMILL_URL = 'https://api.paymill.com/v2/'
PAYMILL_OFFER_ID = 'offer_7aafd70596c34e87335c'

from base import *  # noqa


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory://grandma',
    }
}

INSTALLED_APPS += (
    'discover_runner',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',  # This break tests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = DJANGO_ROOT
TEST_DISCOVER_ROOT = DJANGO_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/grandma.mail'
DEFAULT_FROM_EMAIL = 'django@grandma'
MAILING_CAMPAIGN_HEADER = 'X-Mailjet-Campaign'

NEXMO_API = 'http://rest.nexmo.com/sms/json'
NEXMO_USERNAME = 'username'
NEXMO_PASSWORD = 'password'
NEXMO_FROM = 'Grandma'

PAYMILL_PUBLIC_KEY = '17525186687258c77db2ac5ba2a940d6'
PAYMILL_PRIVATE_KEY = 'cd3ddf7e028d1a8790b6605022153074'
PAYMILL_URL = 'https://api.paymill.com/v2/'
PAYMILL_OFFER_ID = 'offer_7aafd70596c34e87335c'

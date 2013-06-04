from base import *


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'memory://grandma', # Or path to database file if using sqlite3.
    }
}

INSTALLED_APPS += (
    'casper',
    'discover_runner',
)


TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT
TEST_DISCOVER_ROOT = PROJECT_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"

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

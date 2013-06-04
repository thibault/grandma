DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'memory://grandma', # Or path to database file if using sqlite3.
    }
}

APPS = (
    'casper',
)

INSTALLED_APPS += APPS

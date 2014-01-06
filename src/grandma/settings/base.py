# -*- coding: utf-8 -*-

from logging.handlers import SysLogHandler
from os.path import basename
from sys import path
from unipath import Path


########## PATH CONFIGURATION

# Absolute filesystem path to the Django project directory
DJANGO_ROOT = Path(__file__).ancestor(3)

# Absolute filesystem path to the top-level project folder
PROJECT_ROOT = DJANGO_ROOT.ancestor(1)

# Site name
SITE_NAME = basename(PROJECT_ROOT)

# Path to public files (served by the web server)
PUBLIC_ROOT = PROJECT_ROOT.child('public')

# Path to the project Configuration app
CONFIGURATION_APP_ROOT = Path(__file__).ancestor(2)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
path.append(CONFIGURATION_APP_ROOT)


########## DEBUG CONFIGURATION

DEBUG = False
TEMPLATE_DEBUG = DEBUG


########## MANAGER CONFIGURATION

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


########## DATABASE CONFIGURATION

DATABASES = {
    'default': {
    }
}


########## GENERAL CONFIGURATION

LOGIN_URL = '/account/login'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGES = (
    ('en', 'English'),
    ('fr', 'Français'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


########## MEDIA AND STATIC CONFIGURATION

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PUBLIC_ROOT.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PUBLIC_ROOT.child('static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    DJANGO_ROOT.child('static'),
)

#LOCALE_PATHS = (
#    join(DJANGO_ROOT, 'locale'),
#)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


########## SECURITY CONFIGURATION

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^@3q1=p9h)wcs00!cmz3+1)(0k$7a3dvzg621-qwt$j#vgrmfz'


########## TEMPLATE CONFIGURATION

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    DJANGO_ROOT.child('templates'),
)


########## MIDDLEWARE CONFIGURATION

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


########## URL CONFIGURATION

ROOT_URLCONF = 'grandma.urls'


########## APP CONFIGURATION

LOCAL_APPS = (
    'reminders',
    'accounts',
    'contacts',
    'pages',
    'analytics',
)

THIRD_PARTY_APPS = (
    'annoying',
    'django_tables2',
    'widget_tweaks',
    'nexmo',
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


########## LOGGING CONFIGURATION

# See http://www.miximum.fr/bien-developper/876-an-effective-logging-strategy-with-django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[grandma] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': '/dev/log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


########## WSGI CONFIGURATION

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'grandma.wsgi.application'


########## PIPELINE CONFIGURATION

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/project.css',
        ),
        'output_filename': 'css/base.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/jquery.js',
            'js/bootstrap.js',
        ),
        'output_filename': 'js/base.js',
    },
}
########## END PIPELINE CONFIGURATION


########## MISC CONFIGURATION

AUTH_USER_MODEL = 'accounts.User'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

import os.path

import magicranker._private as private

is_dev = os.uname()[1] in private.DEV_SERVERS

# Display debug info if this is a dev server
if is_dev:
    DEBUG = True
else:
    DEBUG = False

ADMINS = (
    (private.ADMIN_FULLNAME, private.ADMIN_EMAIL),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': private.DB_NAME,
    }
}

if is_dev:
    DATABASES['default']['HOST'] = private.DEV_DB_HOST
    DATABASES['default']['USER'] = private.DEV_DB_USER
    DATABASES['default']['PASSWORD'] = private.DEV_DB_PASS
else:
    DATABASES['default']['HOST'] = private.PROD_DB_HOST
    DATABASES['default']['USER'] = private.PROD_DB_USER
    DATABASES['default']['PASSWORD'] = private.PROD_DB_PASS

TIME_ZONE = private.TIME_ZONE

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'assets/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'djangobower.finders.BowerFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = private.SECRET_KEY

# List of callables that know how to import templates from various sources.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

BOWER_COMPONENTS_ROOT = os.path.join(os.path.dirname(__file__), 'assets')

ROOT_URLCONF = private.ROOT_URLCONF

WSGI_APPLICATION = 'magicranker.wsgi.application'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
        'debug': DEBUG
    }
}]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'djangobower',
    'compressor',
    'django_pandas',
    'raven.contrib.django.raven_compat',
    'magicranker.rank',
    'magicranker.home',
    'magicranker.api',
    'magicranker.stock',
    'magicranker.backend',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': private.MEMCACHED_LOCATION,
    }
}

EMAIL_HOST = private.EMAIL_HOST
EMAIL_PORT = private.EMAIL_PORT
DEFAULT_FROM_EMAIL = private.DEFAULT_FROM_EMAIL

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = private.ALLOWED_HOSTS

# Django Bootup configuration settings
BOOTUP_SUPERUSER_NAME = private.SUPERUSER_NAME
BOOTUP_SUPERUSER_PASSWORD = private.SUPERUSER_PASSWORD
BOOTUP_SUPERUSER_EMAIL = private.SUPERUSER_EMAIL

GA_TRACKING_ID = private.GA_TRACKING_ID

BOWER_INSTALLED_APPS = (
    'jquery#1.10',
    'bootstrap#3.2.0',
    'less',
    'angular#<2',
    'angular-bootstrap#0.11.0',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'formatter': 'standard',
            'class':'logging.StreamHandler',

        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

if not is_dev:
    RAVEN_CONFIG = {'dsn': private.RAVEN_DSN}
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True

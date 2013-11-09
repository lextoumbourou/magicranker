import os.path

import _private as private

is_dev = os.uname()[1] in private.DEV_SERVERS

# Display debug info if this is a dev server
if is_dev:
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (private.ADMIN_FULLNAME, private.ADMIN_EMAIL),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': private.DB_ENGINE,
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
    os.path.join(os.path.dirname(__file__), 'templates/static/'),
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
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

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

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'magicranker.context_processors.google_analytics'
)

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
    'south',
    'django_pandas',
    'magicranker.rank',
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

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
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
    'bootstrap',
    'less',
    'angular#1.2.0-rc.3',
    'angular-bootstrap',
    'angular-percentage-filter',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

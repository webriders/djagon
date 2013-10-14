# Django settings for djagon project.

import sys
import os

# WebRiders custom setting
SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Connect applications from 'source' directory
sys.path.insert(0, os.path.join(SITE_ROOT, "source"))

SECRET_KEY = '-lr8jl+feif5gt9m+_t2k-e@1=!5!h3)&u#c@_nrxl50jy9+)r'
SITE_ID = 1

# Media files
MEDIA_ROOT = os.path.abspath(os.path.join(SITE_ROOT, 'var', 'media'))
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.abspath(os.path.join(SITE_ROOT, 'var', 'static'))
STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ROOT_URLCONF = 'conf.urls'

# Python dotted path to the WSGI application used by Django's runserver
WSGI_APPLICATION = 'conf.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # djagon source
    'common',
    'home',
    'sockets',
    'storage',
    'uno',
    'ws_uno',

    # third-party source
    'south',
    'compressor',
    'django.contrib.admin',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

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

# django-compressor settings
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'conf.compressor.precompilers.ScssFilter'),
)

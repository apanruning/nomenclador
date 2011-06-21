# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Martin Onetti', 'onetti.martin@gmail.com'),
    ('Matias Iturburu', 'maturburu@gmail.com'),
    ('Francisco Herrero', 'francisco.herrero@gmail.com'),
)

MANAGERS = ADMINS

#SMTP Test Server
#python -m smtpd -n -c DebuggingServer localhost:1025
ACCOUNT_EMAIL_VERIFICATION = True
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nomenclador',
        'USER': '',         # set in local_settings.py
        'PASSWORD': '',     # set in local_settings.py
        'HOST':'',          # set in local_settings.py
        'PORT':''           # set in local_settings.py
    }
}

TIME_ZONE = 'America/Argentina/Cordoba'

LANGUAGE_CODE = 'es-ar'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

OSM_CSV_ROOT = os.path.join(BASE_DIR, 'csv')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    MEDIA_ROOT,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'

DEFAULT_SRID = 900913

SECRET_KEY = 'xg%7r0k+966nuhr*8ls_@bgkf8y*-e2tar_in#9m%v&8r!y5ao'

#Authenticate using email address
AUTHENTICATION_BACKENDS = (
#    "account.email_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)


MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'nomenclador.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)
AUTH_PROFILE_MODULE = "profiles.Profile"
AUTH_PROFILE_ICON = 'icons/home.png'

PAGINATION_DEFAULT_WINDOW = 2

ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 7
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.markup',
    'django.contrib.comments',
    'django.contrib.messages',
    'debug_toolbar',
    'south',
    'compressor',
    'pagination',    
    'voting',
    'tagging',
    'mptt',
    'registration',
    'profiles',
    'banners',
    'djangoosm',
    'maap',
    'cyj_logs',
    'toolsnmt',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False,
}

from local_settings import *

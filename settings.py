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

STATIC_URL = ''

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ADMIN_MEDIA_PREFIX = '/static/admin/'

DEFAULT_SRID = 900913

SECRET_KEY = 'xg%7r0k+966nuhr*8ls_@bgkf8y*-e2tar_in#9m%v&8r!y5ao'

#Authenticate using email address
AUTHENTICATION_BACKENDS = (
#    "account.email_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'announcements.context_processors.site_wide_announcements',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)
AUTH_PROFILE_MODULE = "profiles.Profile"
AUTH_PROFILE_ICON = os.path.join(MEDIA_ROOT, 'icons/home.png')

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
    'django.contrib.gis',
    'django.contrib.markup',
    'django.contrib.comments',
    'django.contrib.messages',
    'south',
    'compress',
    'announcements',
    'pagination',    
    'voting',
    'tagging',
    'mptt',
    'registration',
    'messages',
    'profiles',
    'banners',
    'maap',
    'djangoosm',
    'cyj_logs',
    'toolsnmt',
)

COMPRESS = DEBUG

COMPRESS_CSS = {
    'stylesheets': {
        'source_filenames': (
            'css/base.css',
            'css/style.css', 
            'css/forms.css', 
            'css/autocomplete.css',
        ),
        'output_filename': 'css/stylesheet.css',
            'media': 'all',
    },
    'toolsnmt': {
        'source_filenames': (
            'css/locations_tool.css',
        ),
        'output_filename': 'css/toolsnmt.css',
            'media': 'all',
    },
}

COMPRESS_JS = {
    'scripts': {
        'source_filenames': (
            'js/jquery.min.js', 
            'js/jquery.ui.js', 
            'js/OpenLayers.js', 
            'js/OpenStreetMap.js', 
            'js/dimensions.js', 
            'js/forms.js', 
            'js/jquery.ajaxQueue.js', 
            'js/jquery.autocomplete.js', 
            'js/autocomplete.js', 
            'js/jstree_admin.js', 
            'js/tiny_mce/tiny_mce.js',
            'js/tiny_mce/jquery.tinymce.js',
            'js/texteditoroptions.js', 
            'js/lib/jquery.tree.min.js',
            'js/lib/plugins/jquery.tree.contextmenu.js',
        ),
        'output_filename': 'js/scripts.js',
    },
    'modules': {
        'source_filenames': (
            'modules/base.js',
            'modules/state.js',
            'modules/point.js',
            'modules/multiline.js',
            'modules/area.js',
            'modules/layer.js',
            'modules/init.js',

        ),
        'output_filename': 'js/modules.js',
    }
}


from local_settings import *

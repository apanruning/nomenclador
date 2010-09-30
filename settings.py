import os
#from django.contrib.gis.utils import add_postgis_srs

## Add Google Maps srs. Just in case. If already exists, nothing happens.
#add_postgis_srs(900913)

# Django settings for nomenclador project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Martin Onetti', 'onetti.martin@gmail.com'),
    ('Matias Iturburu', 'maturburu@gmail.com'),
    ('Francisco Herrero', 'francisco.herrero@gmail.com'),
)

MANAGERS = ADMINS

ACCOUNT_EMAIL_VERIFICATION = True
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.sqlite3',
        'NAME': 'nomenclador',
        'USER': '',
        'PASSWORD': '',
        'HOST':'',
        'PORT':''
    }
}

TIME_ZONE = 'America/Cordoba'

LANGUAGE_CODE = 'es-ar'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
OSM_CSV_ROOT = os.path.join(os.path.dirname(__file__), 'csv')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Default Space Projection
DEFAULT_SRID = 900913

# Don't share this with anybody.
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
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'announcements.context_processors.site_wide_announcements',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)
AUTH_PROFILE_MODULE = "profiles.Profile"
AUTH_PROFILE_ICON = os.path.join(MEDIA_ROOT, 'icons/home.png')

PAGINATION_DEFAULT_WINDOW = 2

ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 7
INSTALLED_APPS = (
#    'notification',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.databrowse',
    'django.contrib.gis',
    'django.contrib.markup',
    'django.contrib.comments',
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
)

COMPRESS = not DEBUG

COMPRESS_CSS = {
    'stylesheets': {
        'source_filenames': (
            'css/base.css',
            'css/style.css', 
            'css/forms.css', 
            'css/wmd.css',
            'css/autocomplete.css',
            'css/street_doors.css'
        ),
        'output_filename': 'css/stylesheet.css',
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
            'js/jquery.textarearesizer.js', 
            'js/autocomplete.js', 
            'js/jstree_admin.js', 
            'js/wmd.js',
            'js/showdown.js',
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


#SMTP Test Server
#python -m smtpd -n -c DebuggingServer localhost:1025
from local_settings import *

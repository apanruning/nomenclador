import os

# Django settings for nomenclador project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

ACCOUNT_EMAIL_VERIFICATION = False

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'nomenclador',
        'USER': 'nomenclador',
        'PASSWORD': 'nomenclador',
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
#    "nomenclador.account.email_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'announcements.context_processors.site_wide_announcements',
)

ROOT_URLCONF = 'nomenclador.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)
AUTH_PROFILE_MODULE = "profiles.Profile"

ACCOUNT_REQUIRED_EMAIL = True
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
    'emailconfirmation',
    'announcements',
    'voting',
    'tagging',
    'mptt',
    'microblogging',
    'nomenclador.account',
    'nomenclador.profiles',
    'messages',
    'nomenclador.banners',
    'nomenclador.maap',
    'osm',
)

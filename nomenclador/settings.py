import os

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/Cordoba'

LANGUAGE_CODE = 'es-ar'

# gdal an geos local paths
#INSTANCE_PATH = '/home/fran/repositorios/cyj/instance1/'
#GDAL_LIBRARY_PATH = INSTANCE_PATH + 'parts/gdal/lib/libgdal.so'
#GEOS_LIBRARY_PATH = INSTANCE_PATH + 'parts/geos/lib/libgeos_c.so'

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ACCOUNT_ACTIVATION_DAYS = 3

ROOT_URLCONF = 'nomenclador.urls'

AUTH_PROFILE_MODULE = "accounts.SiteUserProfile"

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.databrowse',
    'django.contrib.gis',
    'django.contrib.markup',
    'tagging',
    'mptt',
    'nomtools',
    'registration',
    'nomenclador.accounts',
    'nomenclador.banners',
    'nomenclador.maap',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    
)



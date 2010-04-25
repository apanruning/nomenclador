from nomenclador.settings import *

ADMINS = (
    ('admin', 'admin@admin.com'),
)
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025


DEBUG=True
TEMPLATE_DEBUG=DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'nomenclador',
        'USER': 'nomenclador',
        'PASSWORD': 'nomenclador',
        'HOST':'localhost',
        'PORT':'5432'
    }
}

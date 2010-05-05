from nomenclador.settings import *

ADMINS = (
    ('admin', 'admin@admin.com'),
)
EMAIL_HOST = '127.0.0.1'
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

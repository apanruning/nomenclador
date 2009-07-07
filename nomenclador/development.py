from nomenclador.settings import *

ADMINS = (
    ('admin', 'admin@admin.com'),
)


DEBUG=True
TEMPLATE_DEBUG=DEBUG

DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'nomenclador'
DATABASE_USER = 'nomenclador'             # Not used with sqlite3.
DATABASE_PASSWORD = 'nomenclador'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'             # Set to empty string for default. Not used with sqlite3.


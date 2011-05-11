Requerimientos
=================

* django
* postgreSQL - postgis
* django-osm



Instalación en ubuntu
=================

Instalar dependencias de los repositorios de ubuntu:

    $ sudo apt-get install gdal-bin postgresql-8.4-postgis

Crear el template_postgis y permitir que otros usuarios puedan crear bases 
de datos con este:
    
    $ sudo su - postgres # cambiamos al usuario postgres para hacer más simple el resto de los comandos

    $ createdb -E UTF8 template_postgis
    $ createlang -d template_postgis plpgsql # Agregando soporte para PLPGSQL 
    $ psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"

Cargar las rutinas PostGIS SQL:

    $ locate postgis.sql
    /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql # puede traer varios resultados
    $ psql -d template_postgis -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql
    $ psql -d template_postgis -f /usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql

Darle permisos a todos los usuarios de alterar columnas de geomtría:

    $ psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
    $ psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
    $ psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"    

Luego podés crear una base de datos que pueda almacenar las columnas de postgis utilizando el template_postgis:

    $ psql:
    postgres=# CREATE DATABASE nomenclador WITH OWNER=nomenclador TEMPLATE=template_postgis;


Crear el entorno de desarrollo:

    $ virtualenv --no-site-packages nmcl
    $ cd nmcl
    $ . bin/activate 
    $ git clone git@github.com:tutuca/nomenclador.git
    $ pip install -r nomenclador/requirements.txt
    
Ahora resta guardar los datos de entorno en local_settings.py, una configuración de ejemplo es:

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'nomenclador',         # tiene que usar el template_postgis 
            'USER': 'nomenclador',         # definir en local_settings.py
            'PASSWORD': 'nomenclador',     # definir en local_settings.py
            'HOST':'localhost',            # poné otra cosa si sabés lo que estás haciendo
            'PORT':''                      # idem
        }
    }


Correr syncdb pero **NO** crear un super usuario:

    r$ ./manage.py syncdb
    Skipping creation of NoticeTypes as notification app not found
    Syncing...
    Creating tables ...
        ((snip))
    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): no
    Installing custom SQL ...
    Installing indexes ...
        ((snip))
    $ 



    
    
    
    

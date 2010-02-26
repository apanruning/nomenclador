DEVELOPMENT CONFIGURATION
-----------------------------------------------------

#Revisar que mod_wsgi esté instalado
$ sudo apt-get install libapache2-mod-wsgi

#Bajar cyj.buildout
$ git clone git://github.com/tutuca/cyj.buildout.git

# Ejecutar el buildout con staging.cfg como archivo de configuración
$ ./bin/buidout -c staging.cfg

# Yo agregué "nomenclador" como host para que resuelva la ip
$ sudo nano /etc/hosts

>>> 127.0.0.1       localhost
>>> 127.0.1.1       nomenclador

# Dejar el sitio disponible para apache
$ cd /etc/apache2/sites-available/
$ sudo ln -s <path-to-buildout>/etc/nomenclador.conf

# Activarlo
$ cd ..
$ cd sites-enabled
$ sudo ln -s ../sites-available/nomenclador.conf

# Reiniciar apache
$ sudo apache2ctl restart

$ Sincronizamos la base de datos (dentro de la carpeta cyj.buildout)
$ ./bin/django syncdb

PRODUCTION CONFIGURATION
--------------------------------------------------
El día del deployment en comercio y justicia sería:

#Revisar que mod_wsgi esté instalado
$ sudo apt-get install libapache2-mod-wsgi

#Bajar cyj.buildout
$ git clone git://github.com/tutuca/cyj.buildout.git

# correr el buildout como en producción
$ ./bin/buildout -c production.cfg

# Dejar el sitio disponible para apache
$ cd /etc/apache2/sites-available/
$ sudo ln -s <path-to-buildout>/etc/nomenclador.conf

# Activarlo
$ cd ..
$ cd sites-enabled
$ sudo ln -s ../sites-available/nomenclador.conf

# Reiniciar apache
$ sudo apache2ctl restart

El archivo production.cfg ya está configurado con la dirección ip y el nombre de servidor que tenemos andando en comercio y justicia así que debería funcionar como remplazo de pecho

DATABASE INSTALL

#Instalar geodjango y osmosis
 * Osmosis trunk version (http://wiki.openstreetmap.org/wiki/Osmosis_PostGIS_Setup)
 * GeoDjango (http://geodjango.org/docs/install.html)
 
#Crear dos bases de datos: una para calles (osmosis) y otra para datos de aplicacion (nomenclador)

#Crear estructura de osmosis
$ psql -d osmosis_database_name -U database_user -h localhost < <osmosis-trunk>/script/pgsql_simple_schema_0.6.sql 

#Ejecutar comando osmosis 
$ <osmosis-trunk>/bin/osmosis --read-xml file="inputfile.osm" --write-pgsql user="user" password="pass" 
database="database_name" 

donde inputfile.osm es un archivo con el mapa

#Correr osmosis2osmdjango_csv.sql desde la base de datos de calles
$ psql -d osmosis_database_name -U nomenclador -h localhost < <osmosis-django-osm-path>/osmosis2osmdjango_csv.sql

#Correr osmosis2osmdjango_csv.sql desde la base de datos de la aplicacion
$ psql -d nomenclador_database_name -U nomenclador -h localhost < <osmosis-django-osm-path>/osmdjango_csv_import.sqlsv.sql

#Correr shell desde carpeta de cyj.buildout
$ ./bin/django shell

#Ejecutar 
>>>> from osm.utils.model import set_streets, set_doors
>>>> set_streets()
>>>> set_doors()

#Agregar proyeccion google a postgis
#Dentro de la shell anterior, ejecutar
>>>> from django.contrib.gis.utils import add_postgis_srs
>>>> add_postgis_srs(900913)

#Correr servidor
$ ./bin/django runserver






 









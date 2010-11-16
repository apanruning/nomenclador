DATABASE INSTALL
--------------------------------

#Instalar geodjango y osmosis
 * Osmosis trunk version (http://wiki.openstreetmap.org/wiki/Osmosis_PostGIS_Setup)
 * GeoDjango (http://geodjango.org/docs/install.html)
 
#Crear dos bases de datos: una para calles (osmosis). Utilizar el comando createdb como se indica a continuacion
$ sudo su postgres -
<postgres>$ createdb -T template_postgis database_name

#Crear estructura de osmosis
$ psql -d osmosis_database_name -U database_user -h localhost < <osmosis-trunk>/script/pgsql_simple_schema_0.6.sql 

#Ejecutar comando osmosis 
$ <osmosis-trunk>/bin/osmosis --read-xml file="inputfile.osm" --write-pgsql user="user" password="pass" 
database="database_name" 

donde inputfile.osm es un archivo con el mapa

#Correr osmosis2osmdjango_csv.sql desde la base de datos de calles
$ psql -d osmosis_database_name -U nomenclador -h localhost < <osmosis-django-osm-path>/osmosis2osmdjango_csv.sql

#Correr osmdjango_csv_import.sql desde la base de datos de la aplicacion
$ psql -d nomenclador_database_name -U nomenclador -h localhost < <osmosis-django-osm-path>/

#Correr shell en toolsnmt
#Ejecutar 

>>>> from osm.utils.model import set_streets, set_doors
>>>> from django.contrib.gis.utils import add_postgis_srs
>>>> add_postgis_srs(900913)
>>>> set_streets()
>>>> set_doors()

APPLICATION INSTALL
----------------------

# Descargamos el archivo de requerimientos
$ wget http://github.com/monetti/toolsnmt/raw/master/requirements.txt

# Creamos un virtualenv con los paquetes necesarios, yo lo llamé tools_env, pero pueden llamarlo como les plazca
$ pip install -r requirements.txt -E tools_env

# Descargamos toolsnmt,  yo lo descargué en el vitualenv, pero ustedes pueden descargarlo en donde les plazca
$ cd tools_env
$ git clone git@github.com:monetti/toolsnmt.git

# Activamos el entorno y corremos el servidor de pruebas
$ source ../bin/activate
$ ./manage.py runserver




DATABASE INSTALL

#Instalar geodjango
 * GeoDjango (http://geodjango.org/docs/install.html)
 
#Crear dos bases de datos: una para logs (logs_nomenclador) y otra para datos de aplicacion (nomenclador) Utilizar el comando createdb como se indica a continuacion
$ sudo su postgres -
<postgres>$ createdb -T template_postgis database_name



#Correr shell en cyj.buildout
#Ejecutar 
>>>> from osm.utils.model import inport_and_update
>>>> inport_and_update("inputfile.osm")

donde inputfile.osm es un archivo con el mapa

#Para cargar las areas en formato gpx, ejecuter en la shell de cyj.buildout (barrios)
>>>> from maap.utils import import_areas
>>>> from maap.models import MaapCategory
>>>> category = MaapCategory.objects.filter(name='Barrios')
>>>> import_areas('<path_barrio_gpx>', zone=True, categories = category)


DEVELOPMENT CONFIGURATION
-----------------------------------------------------

#Revisar que mod_wsgi esté instalado
$ sudo apt-get install libapache2-mod-wsgi

#Bajar cyj.buildout
$ git clone git://github.com/tutuca/cyj.buildout.git

# Ejecutar el buildout con staging.cfg como archivo de configuración
$ ./bin/buildout

# Sincronizamos la base de datos (dentro de la carpeta cyj.buildout). 
#BUG: Elegir NO CREAR SUPERUSUARIO ya que hay un bug en este punto. Ver el siguiente paso
$ ./bin/django syncdb

#Crear superusuario para la administracion del entorno
$ ./bin/django createsuperuser

#Agregar proyeccion google a postgis
#Dentro de la shell, ejecutar
>>>> from django.contrib.gis.utils import add_postgis_srs
>>>> add_postgis_srs(900913)

#Correr servidor
$ ./bin/django runserver

PRODUCTION CONFIGURATION
--------------------------------------------------
El día del deployment en comercio y justicia sería:

#Revisar que mod_wsgi esté instalado
$ sudo apt-get install libapache2-mod-wsgi

#Bajar y actualizar, cyj.buildout, nomenclador y osm
$ git clone git://github.com/tutuca/cyj.buildout.git
<nomenclador-path>$ git pull
<osm-path>$ git pull

# correr el buildout como en producción
$ ./bin/buildout -c production.cfg

# Dejar el sitio disponible para apache
$ cd /etc/apache2/sites-available/
$ sudo ln -s <path-to-buildout>/etc/conf

# Activarlo
$ cd ..
$ cd sites-enabled
$ sudo ln -s ../sites-available/conf

# Reiniciar apache
$ sudo apache2ctl restart

El archivo production.cfg ya está configurado con la dirección ip y el nombre de servidor que tenemos andando en comercio y justicia así que debería funcionar como remplazo de pecho









 









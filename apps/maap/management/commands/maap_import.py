from django.contrib.gis.geos import Point, LineString,MultiLineString, Polygon, GEOSGeometry
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.core.management.base import BaseCommand, CommandError
from maap.models import MaapZone, MaapArea, MaapPoint, MaapMultiLine, MaapCategory, Icon
from osm.parser import OSMXMLFile
from settings import DEFAULT_SRID
from djangoosm import OSM_SRID
from django.db import connection, transaction

class Command(BaseCommand):
    args = '<osm_file>'
    help = 'Take an .osm file and imports to maap'
    
    @transaction.commit_on_success
    def handle(self, osmfile=None, **options):
        print "Opening %s ..." % osmfile
        osmobject = OSMXMLFile(osmfile)
        
        maap_multilines = {}
        points_count = areas_count = zones_count = 0                

        print "Importing Maap Nodes ..."
        for node in osmobject.nodes.values():
            if node.tags.get('type', None) != 'point':
                continue
            geom = Point(float(node.lon),float(node.lat), srid=OSM_SRID)
            
            if OSM_SRID != 'EPSG:%d' % DEFAULT_SRID:
                geom = osm_change_srid(geom, 'EPSG:%d' % DEFAULT_SRID)
                
            category = get_or_create_category(node.tags['category'])
            if node.tags.has_key('icon'):
                icon = Icon.objects.get(name = node.tags['icon'])
            else:
                icon = Icon.objects.latest('id')
            maap_point, created = MaapPoint.objects.get_or_create(
                name = node.tags['name'],
                defaults = dict(
                    geom = geom,
                    creator_id = 1,
                    editor_id = 1,
                    icon = icon,
                    description = node.tags.get('description', None)
                )
            )
            if not(created):
                maap_point.geom = geom
            maap_point.save()
            maap_point.category.add(category)
            points_count += 1
            
        print "Importing Maap Ways ..."
        for way in osmobject.ways.values():
            pgeom = map(lambda p: (float(p.lon),float(p.lat)), way.nodes)
            if way.tags.get('type', None) == 'multiline':
                geom = LineString(pgeom)
                
                if OSM_SRID != 'EPSG:%d' % DEFAULT_SRID:
                    geom = osm_change_srid(geom, 'EPSG:%d' % DEFAULT_SRID)
                
                if maap_multilines.has_key(way.tags['name']):
                    maap_multilines[way.tags['name']][0].geom.append(geom)
                else:
                    category = get_or_create_category(way.tags['category'])           
                    maap_multiline, created = MaapMultiLine.objects.get_or_create(
                        name = way.tags['name'],
                        defaults = dict(
                            geom = MultiLineString([geom]),
                            creator_id = 1,
                            editor_id = 1,
                            description = way.tags.get('description', None)
                        )                        
                    )
                    if not(created):
                        maap_multiline.geom = MultiLineString([geom])
                    maap_multilines[way.tags['name']] = (maap_multiline, category)
                    
            elif way.tags.get('type', None) in ['area','zone']:
                geom = Polygon(pgeom)
                if OSM_SRID != 'EPSG:%d' % DEFAULT_SRID:
                    geom = osm_change_srid(geom, 'EPSG:%d' % DEFAULT_SRID)

                category = get_or_create_category(way.tags['category'])           
                
                if way.tags['type'] == 'area':
                    maap_area, created = MaapArea.objects.get_or_create(
                        name = way.tags['name'],
                        defaults = dict(
                            geom = geom,
                            creator_id = 1,
                            editor_id = 1,
                            description = way.tags.get('description', None)
                        )                        
                    ) 
                    if not(created):
                        maap_area.geom = geom
                    maap_area.save()
                    maap_area.category.add(category)
                    areas_count += 1
                else:
                    maap_zone, created = MaapZone.objects.get_or_create(
                        name = way.tags['name'],                   
                        defaults = dict(
                            geom = geom,
                            creator_id = 1,
                            editor_id = 1,
                        )                        
                    )
                    if not(created):
                        maap_zone.geom = geom
                    maap_zone.save()
                    maap_zone.category.add(category)
                    zones_count += 1
        
        for maap_multiline, category in maap_multilines.values():
            maap_multiline.save()
            maap_multiline.category.add(category)
            
        print "Points imported %s" % points_count         
        print "Multilines imported %s" % len(maap_multilines)
        print "Areas imported %s" % areas_count        
        print "Zones imported %s" % zones_count
           

def osm_change_srid(geom, srid):
    """ Converts standard merkartor to desired projection """
    obj = OGRGeometry(geom.wkt)
    obj.srs = OSM_SRID
    obj.transform_to(SpatialReference(srid))
    return obj.geos

def get_or_create_category(category_label):
    categories = category_label.split('/')
    parent = None
    for category_name in categories:
        defaults={'parent': parent}
        category, created = MaapCategory.objects.get_or_create(name = category_name,defaults=defaults)
        if created:
            print "Created New Category: %s " % category_name
        parent = category
    return category


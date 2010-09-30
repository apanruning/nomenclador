from django.contrib.gis.geos import Point, LineString,MultiLineString, Polygon, GEOSGeometry
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.core.management.base import BaseCommand, CommandError
from maap.models import MaapZone, MaapArea, MaapPoint, MaapMultiLine, MaapCategory
from osm.parser import OSMXMLFile
from settings import DEFAULT_SRID
from djangoosm import OSM_SRID

class Command(BaseCommand):
    args = '<osm_file>'
    help = 'Take an .osm file and imports to maap'

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
                
            category = get_or_create_category(point.tags['category'])
            maap_point = MaapPoint(
                name = point.tags['name'],
                #category = category,
                geom = geom,
                creator_id = 1,
                editor_id = 1,
            )
            maap_point.save()
            points_count += 1
            
        print "Importing Maap Ways ..."
        for way in osmobject.ways.values():
            if way.tags.get('type', None) == 'multiline':
                pgeom = map(lambda p: (float(p.lon),float(p.lat)), way.nodes)
                geom = LineString(pgeom)
                
                if OSM_SRID != 'EPSG:%d' % DEFAULT_SRID:
                    geom = osm_change_srid(geom, 'EPSG:%d' % DEFAULT_SRID)

                if maap_multilines.has_key(way.tags['name']):
                    maap_multilines[way.tags['name']].geom.append(geom)
                else:
                    category = get_or_create_category(way.tags['category'])           
                    maap_multilines[way.tags['name']] = MaapMultiLine(
                        name=way.tags['name'],
                        #category=category,
                        geom=MultiLineString([geom]),
                        creator_id = 1,
                        editor_id = 1,                        
                    )
            elif way.tags.get('type', None) in ['area','zone']:
                geom = Polygon(pgeom)

                if OSM_SRID != 'EPSG:%d' % DEFAULT_SRID:
                    geom = osm_change_srid(geom, 'EPSG:%d' % DEFAULT_SRID)

                category = get_or_create_category(ways.tags['category'])           
                
                if way.tags['type'] == 'area':
                    maap_area = MaapArea(
                        category=category,
                        geom=geom,
                        creator_id = 1,
                        editor_id = 1,                        
                    )
                    maap_area.save()
                    areas_count += 1
                else:
                    maap_zone = MaapZone(
                        category=category,
                        geom=geom,
                        creator_id = 1,
                        editor_id = 1,                        
                    )
                    maap_zone.save()
                    zones_count += 1
        
        for maap_multiline in maap_multilines.values():
            maap_multiline.save()
            
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
    return None
    categories = category_label.split('/')
    parent = None
    for category_name in categories:
        defaults = dict(
            parent = parent
        )

        category, created = MaapCategory.objects.get_or_create(name = category_name, defaults = defaults)
        if created:
            print "Created New Category: %s " % category_name

        parent = category
            
    return category


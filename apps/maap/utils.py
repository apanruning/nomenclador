import xml.sax
from django.contrib.gis.geos import Point, LineString,MultiLineString, Polygon, GEOSGeometry
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from models import MaapZone, MaapArea, MaapPoint, MaapMultiline, MaapCategory

from settings import DEFAULT_SRID

OSM_SRID = 'EPSG:4326'

class OSMXMLMaapFileParser(xml.sax.ContentHandler):
    def __init__(self, containing_obj):
        self.containing_obj = containing_obj
        self.curr_node = None
        self.curr_way = None

    def startElement(self, name, attrs):

        if name == 'node':
            self.curr_node = dict(
                id=attrs['id'],
                lat=attrs['lat'],
                lon=attrs['lon']
            )

        elif name == 'way':
            self.curr_way = dict(
                id = attrs['id'],
                nodes = []
            )

        elif name == 'tag':
            if self.curr_node:
                self.curr_node[attrs['k']] = attrs['v']
            elif self.curr_way:
                self.curr_way[attrs['k']] = attrs['v']

        elif name == "nd":
            assert self.curr_node is None, "curr_node (%r) is non-none" % (self.curr_node)
            assert self.curr_way is not None, "curr_way is None"
            self.curr_way['nodes'].append(attrs['ref'])

    def endElement(self, name):

        if name == "node":
            self.containing_obj.nodes[self.curr_node['id']] = self.curr_node
            self.curr_node = None

        elif name == "way":
            self.containing_obj.ways[self.curr_way['id']] = self.curr_way
            self.curr_way = None


    
class OSMMaapFile(object):
    nodes = {}
    ways = {}
    points = {}
    areas = {}
    zones = {}
    multilines = {}

    def __init__(self, filename, srid=DEFAULT_SRID):
        self.filename = filename
        self.srid = srid
        
        self.__parse()

    def __parse(self):
        """Parse the given XML file"""
        parser = xml.sax.make_parser()
        parser.setContentHandler(OSMXMLMaapFileParser(self))
        parser.parse(self.filename)
        
        # postprocess nodes
        for element in self.nodes.values():
            if element.get('type', None) == 'point':
                geom = Point((float(element['lat']),float(element['lon'])));
                if OSM_SRID != self.srid:
                    geom = self.__osm_change_srid(geom)
                self.points[element['name']] = dict(
                    category=element['category'],
                    geom=geom
                )
                
        # postprocess ways
        for element in self.ways.values():
            points = [self.nodes[p] for p in element['nodes']]
            pgeom = map(lambda p: (float(p['lat']),float(p['lon'])), points)        
            
            if element.get('type', None) == 'multiline':
                geom = LineString(pgeom)
                
                if OSM_SRID != self.srid:
                    geom = self.__osm_change_srid(geom)

                if self.multilines.has_key(element['name']):
                    self.multilines[element['name']]['geom'].append(geom)
                else:
                    self.multilines[element['name']] = dict(
                        category=element['category'],
                        geom=MultiLineString([geom])
                    )
                
            if element.get('type', None) in ['area','zone']:
                geom = Polygon(pgeom)
                
                if OSM_SRID != self.srid:
                    geom = self.__osm_change_srid(geom)
                
                elem = dict(
                    category=element['category'],
                    geom=geom
                )

                if element['type'] == 'area':
                    self.areas[element['name']] = elem
                else:
                    self.zones[element['name']] = elem
                
    def __osm_change_srid(self, geom):
        """ Converts standard merkartor to desired projection """
        obj = OGRGeometry(geom.wkt)
        obj.srs = OSM_SRID
        obj.transform_to(SpatialReference(self.srid))
        return obj.geos

def get_or_create_category(category_label):
    categories = category_label.split('/')
    parent = None
    for category_name in categories:
        kwargs = dict(
            name = category_name, 
            is_public = False,
            parent = parent
        )

        category, created = MaapCategory.objects.get_or_create(**kwargs)
        if created:
            print "Created New Category: %s " % category_name

        parent = category
            
    return category

def import_maap_osm(filepath):
    print "Opening %s ..." % filepath
    osm = OSMMaapFile(filepath)

    if osm.points:
        print "Importing Maap Points"
        for point in osm.points.values():
            category = get_or_create_category(point['category'])
            point = MaapPoint(
                name = point['name'], 
                category = category,
                geom = point['geom']
            )

    if osm.multilines:
        print "Importing Maap Multilines"

    if osm.areas:
        print "Importing Maap Areas"

    if osm.zones:
        print "Importing Maap Zones"

def import_areas(filepath, zone=True, categories= None):
    
    ds = DataSource(filepath)
    
    for e in ds[2]:
        pgeom = OGRGeometry(Polygon(e.geom.coords[0]).wkt)
        pgeom.srs = 'EPSG:4326'
        pgeom.transform_to(SpatialReference('EPSG:900913'))

        kwargs = dict( 
            geom = pgeom.wkt,
            name = e.get('name'),
            creator_id = 1,
            editor_id = 1,
        )
        if zone:
            ma = MaapZone(**kwargs)
        else:
            ma = MaapArea(**kwargs)

        ma.save()

        if categories:
            ma.category = categories
            ma.save()

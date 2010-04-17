from django.utils import simplejson

# Objeto layer

class BaseLayer(object):
    meta = ['id', 'name', 'type']


    def __init__(self, **argv):
        for k,v in argv.iteritems():
            setattr(self, k, v)
    
    def __iter__(self):
        out = dict()
        for e in self.meta:
            out[e] = getattr(self, e, None)
            
        return out.iteritems()
    
    @property
    def json(self):
        if hasattr(self, 'elements'):
            if self.elements:
                self.elements = [dict(x) for x in self.elements]
        return simplejson.dumps(dict(self))
    

class GeoElement(BaseLayer):

    @property
    def geojson(self):
        return simplejson.loads(self.geom.geojson)
    
    @property
    def meta(self):
        return super(GeoElement, self).meta + \
               ['geojson']


class Point(GeoElement):
    type = 'point'

    @property
    def meta(self):
        return super(Point, self).meta + \
               ['icon','closest']


    icon = {
        "url": "/media/icons/info.png", 
        "width": 32, 
        "height": 37
    }


class MultiLine(GeoElement):
    type = 'multiline'

class Area(GeoElement):
    type = 'area'

class Layer(BaseLayer):    
    type = 'layer'
    
    elements = []
    
    @property
    def meta(self):
        return super(Layer, self).meta + \
               ['elements', 'box_size']
        
        
    @property
    def box_size(self):
        if self.elements:
            geom = self.elements[0].geom
            for i in range(1,len(self.elements)):
                geom = geom.union(self.elements[i].geojson)
            return geom.extent   

    
    
    

def show_street(request):
        street = Nodes.objects.get(pk=request.GET('node')).way
        
        points = []
       
        wl = Ways.objects.filter(street__name=street.name)
        wnl = WayNodes.objects.filter(way__in=wl).all()
        
        points = wnl
           
        lpoints = []
        for p in points:
                pgeom = OGRGeometry(p.geom.wkt)
                pgeom.srs = 'EPSG:4326'
                pgeom.transform_to(SpatialReference('EPSG:900913'))
                pcoord = simplejson.loads(pgeom.json)
                lpoints.append({
                  "type": "point",
                  "id": 'point',
                  "name": "pipin",
                  "geojson": pcoord,
                  "icon": {
                    "url": "/media/icons/info.png",
                    "width": 32,
                    "height": 37
                    }
                })
            
        layer = {
                'type': 'layer',
                'id': 'layer-location',
                'elements': lpoints,
                'box_size': None
        } 
    
    

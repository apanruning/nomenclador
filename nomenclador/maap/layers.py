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
        object_dict = dict(self)
        if hasattr(self, 'elements'):
            if self.elements:
                object_dict['elements'] = [dict(x) for x in self.elements]
        return simplejson.dumps(object_dict)
    

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
    center = False
    @property
    def meta(self):
        return super(Point, self).meta + \
               ['icon']

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
        center_object = None
        
        if self.elements:
            first_element = self.elements[0]
            geom = first_element.geom

            if first_element.center:
                center_object = first_element.geom
                
            for i in range(1,len(self.elements)):
                if self.elements[i].center:
                    center_object = self.elements[i].geom
                geom = geom.union(self.elements[i].geom)

            extent = geom.extent

            if center_object is not None:

                centroid = center_object.centroid
                delta_x = max(abs(extent[0]-centroid.get_x()), 
                              abs(extent[2]-centroid.get_x()))
                              
                delta_y = max(abs(extent[1]-centroid.get_y()), 
                              abs(extent[3]-centroid.get_y()))

                extent = ((centroid.get_x() - delta_x),
                          (centroid.get_y() - delta_y),
                          (centroid.get_x() + delta_x),
                          (centroid.get_y() + delta_y),
                         )
            return extent   

    
    
    

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
    
    

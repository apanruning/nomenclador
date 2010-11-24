from django.utils import simplejson

DEFAULT_ICON = {
    "url": "/media/icons/info.png",
    "width": 32,
    "height": 37
}

order = ['area','multiline','point']

class BaseLayer(object):
    meta = ['id', 'name', 'type', 'absolute_url','popup_text']

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
        type_cmp = lambda x, y: cmp(order.index(x['type']),order.index(y['type']))
        object_dict = dict(self)
        if hasattr(self, 'elements'):
            if self.elements:
                elements = [dict(x) for x in self.elements]
                elements.sort(type_cmp)
                object_dict['elements'] = elements
        
        return simplejson.dumps(object_dict)
    
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
                centroid = (
                    center_object.centroid.get_x(),
                    center_object.centroid.get_y()
                )
                delta_x = max(abs(extent[0]-centroid[0]),
                              abs(extent[2]-centroid[0]))
                              
                delta_y = max(abs(extent[1]-centroid[1]),
                              abs(extent[3]-centroid[1]))

                extent = ((centroid[0] - delta_x),
                          (centroid[1] - delta_y),
                          (centroid[0] + delta_x),
                          (centroid[1] + delta_y),
                         )

            # for historical reasons
            margin = 102
            extent = (
                extent[0] - margin,
                extent[1] - margin,
                extent[2] + margin,
                extent[3] + margin
            )
            
            return extent


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
    icon = DEFAULT_ICON
    
    @property
    def meta(self):
        return super(Point, self).meta + \
               ['icon','radius']

class MultiLine(GeoElement):
    type = 'multiline'

class Area(GeoElement):
    type = 'area'




from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from osm.models import *
from osm.utils.search import get_locations_by_intersection, get_location_by_door
from osm.utils.lists import get_streets_list, get_intersection_list
from osm.utils.words import clean_search_street

from django.core import urlresolvers
from django.utils.http import urlquote
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point

def search_streets(request):
    streetname = clean_search_street(request.POST.get('streetname', ''))
    intersection = clean_search_street(request.POST.get('intersection', ''))
    streetnumber = request.POST.get('streetnumber',None)
    intlist = []
    strlist = []
    
    if streetname and intersection and len(streetname)>2 and len(intersection)>2:
        intlist = get_intersection_list(streetname, intersection)
        if len(intlist) == 0:
            # This should be changed with elegant "not found streets"
            raise Http404
            
    elif streetname and len(streetname)>2:
        strlist = get_streets_list(streetname)
        if len(strlist) == 0:
            # This should be changed with elegant "not found streets"
            raise Http404
            
    context = RequestContext(request,{'intlist':intlist, 'strlist':strlist,'POST': request.POST})
    
    
    return render_to_response('maap/streets.html', context_instance=context)
    
def street_location(request):
    if request.method == 'GET':
        params = request.GET        

        if params.has_key('str'):
            if params.has_key('int'):
                # Intersection Case
                points = get_locations_by_intersection(params['str'],params['int'])
                layer = loc_int2layer(points, params['str'], params['int'])
                
            elif params.has_key('door'):
                # Street door Case
                loc = get_location_by_door(params['str'],params['door'])
                if loc:
                    layer = loc_door2layer(loc, params['str'],params['door'])                
                else:
                    layer = loc_str2layer(params['str'])
                
            else:
                # Street alone
                layer = loc_str2layer(params['str'])
                
            return HttpResponse(layer, mimetype='text/json')  
                            
        else:
            raise Http404        
    else:
        raise Http404


def loc_str2layer(strn):
    
    swl = SearchableWay.objects.filter(name=strn)
    wl = [sw.way for sw in swl]
   
    ln = []
    for w in wl:
        ln.append(LineString([u.node.geom for u in w.waynodes_set.all()]))
    
    ml = MultiLineString(ln)
           
    pgeom = OGRGeometry(ml.wkt)
    pgeom.srs = 'EPSG:4326'
    pgeom.transform_to(SpatialReference('EPSG:900913'))
    lpoints = []
    pcoord = simplejson.loads(pgeom.json)
    lpoints.append({
              "type": "multiline",
              "id": 'street_%s' % strn,
              "name": strn,
              "geojson": pcoord,
    
            })
        
    layer = {
            'type': 'layer',
            'id': 'street_%s' % strn,
            'elements': lpoints,
            'box_size': pgeom.extent
    }
        
    return HttpResponse(simplejson.dumps(layer), mimetype='text/json') 

def loc_door2layer(pos, strn, door):
    pgeom = OGRGeometry(pos[0].wkt)
    pgeom.srs = 'EPSG:4326'
    pgeom.transform_to(SpatialReference('EPSG:900913'))
    pcoord = simplejson.loads(pgeom.json)

    layer = {
        'type': 'layer',
        'id': "%s" % (strn),
        'elements': [{
          "type": "point",
          "id": 'approx_location_%s_%s' % (strn, door), 
          "name": "%s %s" % (strn, door),
          "radius": pos[1],
          "geojson": pcoord, 
          "icon": {
            "url": "/media/icons/info.png", 
            "width": 32, 
            "height": 37
            }
        }],
        'box_size': pgeom.extent
    }                
    

    return simplejson.dumps(layer)

def loc_int2layer(points, str1, str2):
    lpoints = []
    i = 0
    mp = None

    for p in points: 

        i += 1
        pgeom = OGRGeometry(p)
        pgeom.srs = 'EPSG:4326'
        pgeom.transform_to(SpatialReference('EPSG:900913'))
        pcoord = simplejson.loads(pgeom.json)

        if not mp:
            mp = pgeom
        else:
            mp.union(pgeom)
                
        lpoints.append({
          "type": "point",
          "id": 'intersection_%d'% i, 
          "name": "%s y %s" % (str1, str2),
          "geojson": pcoord, 
          "icon": {
            "url": "/media/icons/info.png", 
            "width": 32, 
            "height": 37
            }
        })
    
    layer = {
        'type': 'layer',
        'id': "%s_%s" % (str1, str2),
        'elements': lpoints,
        'box_size': mp.extent
    }                    

    return simplejson.dumps(layer)  




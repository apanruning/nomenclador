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
from osm.utils.words import clean_search_street
from django.core import urlresolvers
from django.utils.http import urlquote
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point

def search_streets(request):

    streetnumber = request.POST.get('streetnumber',None)
    
    cs_street = clean_search_street(request.POST.get('streetname', ''))
    cs_inters = clean_search_street(request.POST.get('intersection', ''))
    results=[]
    
    if cs_street and len(cs_street)>2:

        # Intersection Case
        if cs_inters and len(cs_inters)>2:
            
            # This part must be optimized and refactorized
            first = Streets.objects.filter(norm__contains = cs_street)
            for f in first:
                second = f.intersections.filter(norm__contains = cs_inters)
                for s in second:
                    results.append({
                        'name': '%s Int. %s' % (f.name, s.name),
                        'url_params': 'str=%s&int=%s' % (f.id, s.id)
                    })
        
        # Street doors Case
        elif streetnumber is not None and streetnumber.isdigit():
            strlist = Streets.objects.filter(norm__contains = cs_street)
            for s in strlist:
                results.append({
                    'name': '%s %s' % (s.name, streetnumber),
                    'url_params': 'str=%s&door=%s' % (s.id, streetnumber)
                })
        
        # Street alone Case
        else:
            strlist = Streets.objects.filter(norm__contains = cs_street)
            for s in strlist:
                results.append({
                    'name': '%s' % s.name,
                    'url_params': 'str=%s' % s.id
                })

        if len(results) == 0:
            # This should be changed with elegant "not found current search"
            raise Http404
            
    context = RequestContext(request,{'results':results})
    
    return render_to_response('maap/streets.html', context_instance=context)
    
def street_location(request):
    if request.method == 'GET':
        params = request.GET        

        if params.has_key('str'):
            if params.has_key('int'):
                # Intersection Case
                nodes = get_locations_by_intersection(params['str'],params['int'])
                points = [n.geom.wkt for n in nodes] 
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
    
    waylist = Ways.objects.filter(street__id=strn)
   
    ln = []
    for w in waylist:
        nodes = [u.node.geom for u in w.waynodes_set.all()]
        ln.append(LineString(nodes))
    
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
          "geojson": pcoord, 
          "icon": {
            "url": "/media/icons/info.png", 
            "width": 32, 
            "height": 37
            }
        }],
        'box_size': pgeom.extent
    }                

    if pos[1] > 0:    
        layer['elements'][0]["radius"] = pos[1]
          
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




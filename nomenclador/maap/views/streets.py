from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from osm.models import *
from osm.utils import get_locations_by_intersection, get_location_by_door, \
                      get_streets_list, get_intersection_list

from django.core import urlresolvers
from django.utils.http import urlquote



def search_streets(request):
    streetname = request.POST.get('streetname', None)
    intersection = request.POST.get('intersection',None)
    streetnumber = request.POST.get('streetnumber',None)
    intlist = []
    strlist = []
    
    if streetname and intersection and len(streetname)>2 and len(intersection)>2:
        intlist = get_intersection_list(streetname, intersection)
        if len(intlist) == 0:
            # This should be changed with elegant "not found streets"
            raise Http404
        elif len(intlist) == 1:
            # This should redirect to answer
            args = '?str=%s&int=%s'%(urlquote(intlist[0][0]),urlquote(intlist[0][1]))
            return redirect(urlresolvers.reverse(street_location)+args)

    elif streetname and streetnumber and len(streetname)>2:
        strlist = get_streets_list(streetname)
        if len(strlist) == 0:
            # This should be changed with elegant "not found streets"
            raise Http404
        elif len(strlist) == 1:
            # This should redirect to answer
            args = '?str=%s&door=%s'%(urlquote(strlist[0][0]),streetnumber)
            return redirect(urlresolvers.reverse(street_location)+args)
            
    context = RequestContext(request,{'intlist':intlist, 'strlist':strlist,'POST': request.POST})
    
    
    return render_to_response('maap/streets.html', context_instance=context)
    
def street_location(request):
    if request.method == 'GET':
        params = request.GET        
        points = []
        if params.has_key('str'):
            if params.has_key('int'):
                points += (get_locations_by_intersection(params['str'],params['int']))
                
            elif params.has_key('door'):
                loc = get_location_by_door(params['str'],params['door'])
                if loc:
                    points.append(loc[0].wkt)
            else:
                raise Http404

            if params.has_key('out'):
                out = params['out']
                if out == 'layer' and points:
                    lpoints = []
                    for p in points: 
                        pgeom = OGRGeometry(p)
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
                    return HttpResponse(simplejson.dumps(layer), mimetype='text/json')  
                else:
                    raise Http404
            
            else:
                path = request.get_full_path() + '&out=layer'
                context = RequestContext(request, {'params': params, 'layerpath':path})
                return render_to_response('maap/street_location.html', context_instance=context)               
                
        else:
            raise Http404        
    else:
        raise Http404


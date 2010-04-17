from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from nomenclador.maap.models import Streets, Nodes
from osm.models import StreetIntersection, Ways
from osm.utils.search import get_location_by_door
from osm.utils.words import clean_search_street
from django.core import urlresolvers
from django.utils.http import urlquote
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point

def search_streets(request):

    streetnumber = request.POST.get('streetnumber',None)
    cs_street = clean_search_street(request.POST.get('streetname', ''))
    cs_inters = clean_search_street(request.POST.get('intersection', ''))
    with_intersection = False
    if cs_street and len(cs_street)>2:

        # Intersection Case
        if cs_inters and len(cs_inters)>2:
            # Reworked version with only one query
            street_list = StreetIntersection.objects.filter(first_street__norm__contains=cs_street,                                                             second_street__norm__contains=cs_inters)
            with_intersection = True
            queryterm = '%s y %s' %(cs_street, cs_inters)

        # Street doors Case
        elif streetnumber is not None and streetnumber.isdigit():
            street_list = Streets.objects.filter(norm__contains = cs_street)
            queryterm = '%s al %s' %(cs_street, streetnumber)

        # Street alone Case
        else:
            street_list = Streets.objects.filter(norm__contains = cs_street)
            queryterm = '%s' %(cs_street)

        if not street_list:
            # This should be changed with elegant "not found current search"
            raise Http404
            
    return object_list(request,
                        street_list,
                        template_name='maap/streets.html',
                        extra_context={'with_intersection':with_intersection,
                                       'streetnumber':streetnumber,
                                       'queryterm':queryterm})
    
def street_location(request):
    if request.method == 'GET':
        params = request.GET        
        streetnumber = params.get('door',None)
        street = None
        if params.has_key('str'):
            if params.has_key('int'):
                # Intersection Case
                nodes = Nodes.objects.filter(waynodes__way__street__norm = params['str'])
                nodes = nodes.filter(waynodes__way__street__norm = params['int'])
                layer = nodes[0].to_layer()
                layer.name = "%s %s" % (params['str'], params['int'])
                json_layer = layer.json

            elif params.has_key('door'):
                # Street door Case
                street = Streets.objects.get(norm = params['str'])
                layer = street.get_location_or_street(door = params['door'])
                json_layer =layer.json

            else:
                # Street alone
                street = Streets.objects.get(norm=params['str'])
                layer = street.to_layer() 
                json_layer = layer.json
            context = RequestContext(request,{ 
                    'json_layer':json_layer, 
                    'street':street,
                    'streetnumber':streetnumber
                    })
            return render_to_response('maap/street_detail.html', context_instance = context)
                            
        else:
            raise Http404        
    else:
        raise Http404



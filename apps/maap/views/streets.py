from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from maap.models import Streets, Nodes
from djangoosm.models import StreetIntersection, Ways
from djangoosm.utils.search import get_location_by_door
from djangoosm.utils.words import clean_search_street
from django.core import urlresolvers
from django.utils.http import urlquote, urlencode
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point
from cyj_logs.models import SearchLog
import logging

def search_streets(request):
    streetnumber = request.GET.get('streetnumber',None)
    cs_street = clean_search_street(request.GET.get('streetname', ''))
    cs_inters = clean_search_street(request.GET.get('intersection', ''))
    with_intersection = False
    if cs_street and len(cs_street)>2:
        # Intersection Case
        if cs_inters and len(cs_inters)>2:
            # Reworked version with only one query
            street_list = StreetIntersection.objects.filter(
                first_street__norm__contains  = cs_street,
                second_street__norm__contains = cs_inters
            )
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
            
        if street_list.count() == 1:
            # Stand Alone case
            params = {}
            if with_intersection:
                params['str'] = street_list[0].first_street.norm
                params['int'] = street_list[0].second_street.norm
            else:
                params['str'] = street_list[0].norm
            if streetnumber:
                params['door'] = streetnumber
            
            url = "%s?%s" % (urlresolvers.reverse('maap.views.street_location'), 
                             urlencode(params))
                                 
            return  HttpResponseRedirect(url)
            
        #In this case log a fail search
        if street_list.count() == 0:
            ty_sch = 0
            if streetnumber:
                message = 'NO EXITO: %s %s' % (cs_street, streetnumber)
                ty_sch = "calle_altura"
            
            if cs_inters: 
                message = 'NO EXITO: %s %s' % (cs_street, cs_inters)
                ty_sch = "calle_interseccion"
            
            if cs_street:
                message = 'NO EXITO: %s' % cs_street
                ty_sch = 'calle'
                
            url = '%s' %(request.get_full_path())
            
            slog = SearchLog(message=message,url=url,tuvo_exito=False,type_search=ty_sch,level=20)
            slog.save()
            
        return object_list(
            request,
            street_list,
            template_name='maap/streets.html',
            extra_context={'with_intersection':with_intersection,
                           'streetnumber':streetnumber,
                           'queryterm':queryterm})
                           
    return redirect('index')
    
def street_location(request):
    if request.method == 'GET':
        params = request.GET
        streetnumber = params.get('door', None)
        street = None
        #Variables for log case in database
        message = "" 
        ty_sch = 0 #Type of search
        success = True
        if params.has_key('str'):
            if params.has_key('int'):
                # Intersection Case
                ## FIXME: Do it more efficient, avoiding 2 queries
                street = StreetIntersection.objects.filter(first_street__norm = params['str'])
                street = street.filter(second_street__norm = params['int'])[0]
                nodes = Nodes.objects.filter(waynodes__way__street__norm = params['str'])
                nodes = nodes.filter(waynodes__way__street__norm = params['int'])
                layer = nodes[0].to_layer()
                layer.name = "%s %s" % (params['str'], params['int'])
                json_layer = layer.json
                message = 'EXITO: %s %s' %(params['str'], params['int'])
                ty_sch = "calle_interseccion"
                
            elif params.has_key('door'):
                # Street door Case
                street = Streets.objects.get(norm = params['str'])
                #import ipdb; ipdb.set_trace()
                layer,success = street.get_location_or_street(door = params['door'])
                ty_sch = "calle_altura"
                json_layer = layer.json
                if success:
                    message = 'EXITO: %s %s' %(params['str'], params['door'])
                else:
                    message = 'NO EXITO: %s %s' %(params['str'], params['door'])
            else:
                # Street alone
                street = Streets.objects.get(norm=params['str'])
                layer = street.to_layer() 
                json_layer = layer.json
                message = 'EXITO: %s' % params['str']
                ty_sch = "calle"
                
            url = '%s' %(request.get_full_path()) 

            #Log a succesfully case
            slog = SearchLog(message=message,url=url,level=20,tuvo_exito=success,type_search=ty_sch)
            slog.save()                

                
            
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



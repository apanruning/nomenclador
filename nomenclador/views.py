from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from osm.models import *
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext


#def doors(request):
#    sw = SearchableWay.objects.all()
            
#    context = RequestContext(request,{'streets':sw })
    
    
#    return render_to_response('street_doors.html', context_instance=context)    

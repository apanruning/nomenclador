from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import create_update
from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import Distance, D
from django.core import urlresolvers
from django.utils.http import urlquote
from nomenclador.maap.models import MaapModel, MaapPoint, MaapArea, \
                                    MaapMultiLine, Icon, MaapCategory
from tagging.models import TaggedItem, Tag

def index(request,*args, **kwargs):
    queryset = MaapModel.objects.all()
    return object_list(
        request, 
        queryset, 
        paginate_by=5,
        *args,**kwargs)
    
##Generic Views
def view(request,cat_slug, object_id):
    objects = MaapModel.objects.filter(category__slug=cat_slug)
    category = MaapCategory.objects.get(slug=cat_slug)  
    obj = objects.get(id = object_id)
    geom = obj.cast().geom        
        
    json_layer = obj.cast().to_layer().json
    
    return object_detail(
        request, 
        objects, 
        int(object_id),
        extra_context = {'category':category, 
                         'object_list':objects, 
                         'json_layer': json_layer
                        },
        template_name = 'maap/object_detail.html')

@login_required  
def edit(request, model, slug=None):
    modelm = get_model('maap',model)
    return create_update.update_object(
        request, 
        model=model, 
        slug=slug, 
        template_name='maap/object_form.html',
        extra_context={'model':model.__name__})  

@login_required
def create(request, model):
    model = get_model('maap',model)
    return create_update.create_object(
        request, 
        model=model,
        template_name='maap/object_form.html',
        extra_context={'model':model.__name__})


def get_objects(request):
    if request.method == 'GET':
        params = request.GET        
        object_list = MaapModel.objects.all()

        if params.has_key('id'):
            object = object_list.get(pk = int(params['id']))
            layer = object.cast().to_layer().json
        
        #if params.has_key('searchterm'):
        #    object_list &= MaapModel.objects.filter(name__icontains=params['searchterm'])

        #if params.has_key('category'):
        #    try:
        #        catel = MaapCategory.objects.get(slug = params['category'])
        #    except MaapCategory.DoesNotExist:
        #        raise Http404
        #    qscats = catel.get_descendants(include_self=True)
        #    object_list = object_list.filter(category__in=qscats)
            
        #if params.has_key('tag'):
        #    object_list &= TaggedItem.objects.get_by_model(MaapModel, params['tag'])
                    
        if params.has_key('out'):
            out = params['out']
            if out == 'layer':
                
                return HttpResponse(simplejson.dumps(layer), mimetype='text/json')  
            else:
                raise Http404    
        else:
            path = request.get_full_path() + '&out=layer'
            return object_list(request,
                                object_list, 
                                'maap/index.html', 
                                paginate_by=5,
                                extra_instance={'layerpath':path})
    else:
        raise Http404

def obj_list_by_cat(request, cat_slug):
    try:
        catel = MaapCategory.objects.get(slug = cat_slug)
    except MaapCategory.DoesNotExist:
        raise Http404
        
    qscats = catel.get_descendants(include_self=True)
    mmodels = MaapModel.objects.filter(category__in=qscats)
    context = RequestContext(request, {'category':catel, 'object_list':mmodels})
    return render_to_response('maap/index.html', context_instance=context)
    
def obj_list_by_tag(request, tag):
    result = TaggedItem.objects.get_by_model(MaapModel, tag)
    context = RequestContext(request, {'tag':tag , 'objs': result})
    return render_to_response('maap/index.html', context_instance=context)



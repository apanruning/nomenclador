from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import create_update
from nomenclador.maap.models import MaapModel, MaapPoint, MaapArea, MaapMultiLine, Icon, MaapCategory
from django.contrib.auth.decorators import login_required
from tagging.models import TaggedItem, Tag


from django.core import urlresolvers
from django.utils.http import urlquote

def index(request,*args, **kwargs):
   
    queryset = MaapModel.objects.all()
    return object_list(
        request, 
        queryset, 
        *args,**kwargs)
    
##Generic Views
def view(request,cat_slug, object_id):
    objects = MaapModel.objects.filter(category__slug=cat_slug)
    category = MaapCategory.objects.get(slug=cat_slug)   
    return object_detail(
        request, 
        objects, 
        int(object_id), 
        extra_context={'category':category,'object_list':objects},
        template_name='maap/object_detail.html')

def maap_object_detail(request,cat_slug, object_id):
    #FIXME no usar la vista de arriba, hay que ver quien esta llamando esta vista
    # ya que levanta un error cuando la sacas
    pass

@login_required  
def edit(request, model, slug=None):
    modelm = get_model('posts',model)
    return create_update.update_object(
        request, 
        model=model, 
        slug=slug, 
        template_name='maap/object_form.html',
        extra_context={'model':model.__name__})  

@login_required
def create(request, model):
    model = get_model('posts',model)
    return create_update.create_object(
        request, 
        model=model,
        template_name='maap/object_form.html',
        extra_context={'model':model.__name__})


def get_objects(request):

    if request.method == 'GET':
        params = request.GET        
        

        qset = MaapModel.objects.all()

        if params.has_key('id'):
            qset &= MaapModel.objects.filter(pk = int(params['id']))

        if params.has_key('searchterm'):
            qset&= MaapModel.objects.filter(name__icontains=params['searchterm'])

        if params.has_key('category'):
            try:
                catel = MaapCategory.objects.get(slug = params['category'])
            except MaapCategory.DoesNotExist:
                raise Http404
            qscats = catel.get_descendants(include_self=True)
            qset = qset.filter(category__in=qscats)
            
        if params.has_key('tag'):
            qset &= TaggedItem.objects.get_by_model(MaapModel, params['tag'])
        
                
        if params.has_key('out'):
            out = params['out']
            if out == 'layer':
                layer = json_layer(qset)
                return HttpResponse(simplejson.dumps(layer), mimetype='text/json')  
            else:
                raise Http404    
        else:
            path = request.get_full_path() + '&out=layer'
            context = RequestContext(request, {'objs': qset, 'layerpath':path})
            return render_to_response('maap/results.html', context_instance=context)
    else:
        raise Http404
        
def convOSM(wkt):
    """ Converts standard merkartor 
        to osm projection as tuple 
    """
    obj = OGRGeometry(wkt)
    obj.srs = 'EPSG:4326'
    obj.transform_to(SpatialReference('EPSG:900913'))
    #obj.transform_to(SpatialReference('EPSG:4326'))
    return (obj.x, obj.y)

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
    return render_to_response('maap/list_by_tag.html', context_instance=context)



 
def json_layer(qset):
    objects = []
    for mo in qset:
        try:
            objects.append(mo.maappoint)
            continue
        except MaapPoint.DoesNotExist:
            pass
        try:
            objects.append(mo.maapmultiline)
            continue
        except MaapMultiLine.DoesNotExist:
            pass
        try:
            objects.append(mo.maaparea)
            continue
        except MaapArea.DoesNotExist:
            pass
    
    if objects:
        geom = objects[0].geom
        for i in range(1,len(objects)):
            geom = geom.union(objects[i].geom)
        box_size = geom.extent
    else:
        box_size = ''
    
    json_results = [o.json_dict for o in objects]
    layer = {
        'type': 'layer',
        'id': 'layer-object-%s' % 'layer',
        'elements': json_results,
        'box_size': box_size
    }
    return layer
        


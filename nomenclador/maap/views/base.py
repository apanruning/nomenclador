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
from nomenclador.profiles.models import Profile
from nomenclador.maap.models import MaapModel, MaapPoint, MaapArea, \
                                    MaapMultiLine, Icon, MaapCategory
from tagging.models import TaggedItem, Tag
from django.template.defaultfilters import slugify

def index(request,*args, **kwargs):
    queryset = MaapModel.objects.filter(category__isnull=False, category__is_public=True)
    queryset = queryset.distinct()
    return object_list(
        request, 
        queryset, 
        paginate_by=10,
        *args,**kwargs)

def search_people(request):
    if request.method == 'POST':
        term = request.POST['firstname']
        queryset = Profile.objects.filter(name_contains=term)
        return object_list(
            request,
            queryset,
            paginate_by=10,
            template_name='maap/index.html', 
        )


#def search_places(request):
#    return obj_list_by_cat(request)
    
##Generic Views
def view(request,cat_slug, object_id):
    objects = MaapModel.objects.filter(category__slug=cat_slug)
    objects = objects.distinct()
    category = MaapCategory.objects.get(slug=cat_slug)  
    obj = objects.get(id = object_id)
    geom = obj.cast().geom        
        
    json_layer = obj.cast().to_layer().json
    
    return object_list(
        request, 
        objects, 
        paginate_by=10,
        template_name = 'maap/object_detail.html',
        extra_context = {
            'category':category, 
            'object':obj, 
            'json_layer': json_layer
            },
    )

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

def search_places(request, cat_slug=None):
    search_term = request.GET.get('searchterm', None)
    
    objects = MaapModel.objects.all()

    kwargs = dict(
        paginate_by = 10,
        template_name = 'maap/index.html', 
        extra_context = {}
    )

    
    if cat_slug:    
        try:
            category = MaapCategory.objects.get(slug = cat_slug)
        except MaapCategory.DoesNotExist:
            raise Http404
        descendants = category.get_descendants(include_self = True)
        objects = objects.filter(category__in = descendants)

        kwargs['extra_context']['category'] = category
    
    if search_term:
        objects = objects.filter(slug__contains = slugify(search_term))
        #kwargs['extra_context']['params'] = dict(request.GET)
        
    objects = objects.distinct()
        
    return object_list(request, objects, **kwargs)
    
def obj_list_by_tag(request, tag):
    result = TaggedItem.objects.get_by_model(MaapModel, tag)
    context = RequestContext(request, {'tag':tag , 'objs': result})
    return render_to_response('maap/index.html', context_instance=context)



# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import create_update, simple
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import Distance, D
from django.core import urlresolvers
from django.utils.http import urlquote
from profiles.models import Profile
from maap.models import MaapModel, MaapPoint, MaapArea, \
                                    MaapMultiLine, Icon, MaapCategory
from maap.forms import MaapPointForm
from tagging.models import TaggedItem, Tag
from django.template.defaultfilters import slugify
from cyj_logs.models import SearchLog


def index(request,*args, **kwargs):
    queryset = MaapModel.objects.filter(category__isnull=False, category__is_public=True)
    queryset = queryset.distinct()
    return object_list(
        request, 
        queryset,
        extra_context= {'json_layer': queryset.layer().json},       
        *args,**kwargs)

def server_error(request):
    return simple.direct_to_template(request, '500.html')

def not_found(request):
    return simple.direct_to_template(request, '404.html')

def search_people(request):
    term = request.GET.get('firstname', None)
    queryset = Profile.objects.filter(public=True)

    if term:
        queryset = queryset.filter(name__icontains=term)

    objects = MaapPoint.objects.filter(profile__in = queryset)    
    return object_list(
        request,
        queryset,
        template_name = 'maap/people.html', 
        extra_context = {
            'default':'people',
            'json_layer': objects.layer().json
        }          
    )
    
##Generic Views
def view(request,cat_slug, object_id):
    objects = MaapModel.objects.filter(category__slug=cat_slug)
    objects = objects.distinct()
    category = MaapCategory.objects.get(slug=cat_slug)  
    obj = objects.get(id = object_id)
    geom = obj.cast().geom        
    
    json_layer = obj.cast().to_layer().json

    #Log a succesfully case 
    message = 'EXITO: %s' % obj.name
    url = '%s' %(request.get_full_path())
    slog = SearchLog(message=message,url=url,level=20, tuvo_exito=True,type_search="categoria")
    slog.save()

    return object_list(
        request,
        objects, 
        template_name = 'maap/object_detail.html',
        extra_context = {
            'category':category, 
            'object':obj, 
            'json_layer': json_layer,
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
def create(request):
    return create_update.create_object(
        request, 
        model=MaapPoint,
        form_class=MaapPointForm,
        template_name='maap/object_form.html',
    )


def search_places(request, cat_slug=None):
    search_term = request.GET.get('placename', None)
    
    objects = MaapModel.objects.all()

    kwargs = dict(
        template_name = 'maap/places.html', 
        extra_context = {
            'default':'places',
        }      
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
        
    objects = objects.distinct()
    kwargs['extra_context']['json_layer'] = objects.layer().json        
    
    return object_list(request, objects, **kwargs)
    
def obj_list_by_tag(request, tag):
    result = TaggedItem.objects.get_by_model(MaapModel, tag)
    return object_list(
        request, 
        result, 
        template_name='maap/index.html', 
        extra_instance={'tag':tag}
    )

def log_out(request):
    from django.contrib.auth import logout
    logout(request)
    messages.add_message(request, messages.INFO, u'Ha cerrado su sesión')    
    return redirect('index')



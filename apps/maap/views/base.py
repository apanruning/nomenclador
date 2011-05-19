# -*- coding: utf-8 -*-
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response, render
from django.views.generic import create_update
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.gis.measure import Distance, D
from profiles.models import Profile
from maap.models import MaapModel, MaapPoint, MaapArea, \
                                    MaapMultiLine, Icon, MaapCategory
from maap.forms import MaapPointForm
from tagging.models import TaggedItem, Tag
from django.template.defaultfilters import slugify
from cyj_logs.models import SearchLog


def index(request, template_name='maap/index.html'):
    queryset = MaapModel.objects.filter(category__isnull=False, category__is_public=True)
    queryset = queryset.distinct()
    return render(
        request, 
        template_name,
        {
            'object_list': queryset,
        }

    )
def server_error(request):
    return render(request, '500.html')

def not_found(request):
    return render(request, '404.html')

def search_people(request):
    term = request.GET.get('firstname', None)
    queryset = Profile.objects.filter(public=True)
    context = {
        'object_list': queryset,
        'default':'people',
        'search_term': term,
    }

    if term:
        results = queryset.filter(name__icontains=term) 
        objects = MaapPoint.objects.filter(profile__in = results).layer().json
        context['object_list'] = results
        context['objects'] = objects

    return render(
        request,
        'profiles/profile_list.html', 
        context
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

    return render(
        request,
        'maap/object_detail.html',
        {
            'object_list': objects,
            'category':category, 
            'object':obj, 
             'json_layer': json_layer,
        }
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
    context =  {
            'object_list': objects,
            'default':'places',
    }
    
    if cat_slug:    
        try:
            category = MaapCategory.objects.get(slug = cat_slug)
        except MaapCategory.DoesNotExist:
            raise Http404

        context['category'] = category        
        descendants = category.get_descendants(include_self = True)
        objects = objects.filter(category__in = descendants)

        
    if search_term:
        objects = objects.filter(slug__contains = slugify(search_term))
        
    context['objects'] = objects.distinct()
    context['json_layer'] = objects.layer().json        
    
    return render(
        request, 
        'maap/places.html',
        context,
    )
    
def obj_list_by_tag(request, tag):
    result = TaggedItem.objects.get_by_model(MaapModel, tag)
    return render(
        request, 
        'maap/index.html', 
        {
        'object_list':result,
        'tag':tag
        }
    )

def log_out(request):
    from django.contrib.auth import logout
    logout(request)
    messages.add_message(request, messages.INFO, u'Ha cerrado su sesión')    
    return redirect('index')

def barrios(request):
    queryset = MaapModel.objects.filter(category__name='Barrios')
    name = request.GET.get('name')
    if name:
        queryset = queryset.filter(name__istartswith=name)
    return HttpResponse(
        simplejson.dumps([(x.pk, x.name) for x in queryset]), 
        content_type="application/json",
    )

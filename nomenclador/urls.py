from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic import list_detail, create_update
from django.views.generic.simple import direct_to_template
from voting.views import xmlhttprequest_vote_on_object as vote_on_object
from nomenclador.places.models import Place
from settings import MEDIA_ROOT
admin.autodiscover()


handler500 # Pyflakes

urlpatterns = patterns( '',
    (r'^$', 'nomenclador.maap.views.index'),
    (r'^maap/', include('nomenclador.maap.urls')),

    (r'^cuenta/', include('nomenclador.account.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^acerca_de/', direct_to_template, {'template':'about.html'}),
    (r'^mensajes/', include('messages.urls')),
    (r'^notificaciones/', include('notification.urls')),
            
    url(r"^announcements/", include("announcements.urls")),
    url(r'^tags/(?P<tag>[^/]+)/$','nomenclador.places.views.obj_list_by_tag', name='list_by_tag'),
    url(r'^categoria/(?P<cat_slug>[^/]+)/$', 'nomenclador.places.views.obj_list_by_cat', name='list_by_category'),
    url(r'^registrarse/$', 'nomenclador.account.views.signup', name='signup'),
    url(r'^ingresar/$', 'nomenclador.account.views.login', name='login'),
    url(r'^salir/$', 'django.contrib.auth.views.logout', {'template_name': 'account/logout.html'}, name='logout'),
    url(r'^miembros/$', 'nomenclador.profiles.views.profiles', name='profile_list'),
    url(r'^vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, place_dict, name="vote"),
    url(r'^(?P<cat_slug>[^/]+)/(?P<object_slug>[^/]+)/$','nomenclador.places.views.view', name='view'),
    url(r'^(?P<username>[\w\._-]+)/$', 'nomenclador.profiles.views.profile', name='profile_detail'),

)

if settings.DEBUG:

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )

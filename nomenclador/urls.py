from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail, create_update
from django.views.generic.simple import direct_to_template
from voting.views import vote_on_object
from nomenclador.maap.models import MaapModel
from django.conf import settings 
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('nomenclador.maap.views',
    (r'^$', 'index',{'template_name':'maap/index.html'}, 'index'),
    url(r'^categoria/(?P<cat_slug>[^/]+)/$', 'obj_list_by_cat', name='list_by_category'),
    url(r'^api/get$', 'get_objects',name='get_objects'),
    (r'^map/streets/$', 'search_streets'),
    (r'^map/streets/location$', 'street_location'),
    (r'^tags/(?P<tag>[^/]+)/$','obj_list_by_tag'),
)

urlpatterns += patterns( '',
    (r'^cuenta/', include('nomenclador.account.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^acerca_de/', direct_to_template, {'template':'about.html'}),
    (r'^mensajes/', include('messages.urls')),
    (r'^notificaciones/', include('notification.urls')),
    (r"^announcements/", include("announcements.urls")),
    
    )


urlpatterns += patterns('nomenclador',
    url(r'^registrarse/$', 'account.views.signup', name='signup'),

    url(r'^miembros/$', 'profiles.views.profiles', name='profile_list'),
    url(r'^miembros/(?P<username>[\w\._-]+)/$', 'profiles.views.profile', name='profile_detail'),
    url(r'^miembros/(?P<user_id>[\w\._-]+)/edit$', 'profiles.views.profile_edit', name='profile_edit'),
    url(r'^ingresar/$', 'account.views.login', name='login'),
    )

urlpatterns += patterns( '',
    url(r'^salir/$', 'django.contrib.auth.views.logout', {'template_name': 'account/logout.html'}, name='logout'),
    url(r'^vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, dict(model=MaapModel, 
            template_name='confirm_vote.html',
            allow_xmlhttprequest=True),
        name='vote'),
    url(r'^(?P<cat_slug>[^/]+)/(?P<object_id>[^/]+)/$','nomenclador.maap.views.view', name='view'),


)
if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    )

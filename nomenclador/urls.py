from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail, create_update
from django.views.generic.simple import direct_to_template
from voting.views import vote_on_object

from django.conf import settings 
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth import login as auth_login

from nomenclador.maap.models import MaapModel
from nomenclador.profiles.forms import LoginForm

admin.autodiscover()

urlpatterns = patterns('nomenclador.maap.views',
    (r'^$', 'index',{'template_name':'maap/index.html'}, 'index'),
    url(r'^map/streets$', 'search_streets', name='search_streets'),
    url(r'^map/people$', 'search_people', name='search_people'),
    url(r'^map/places$', 'search_places', name='search_places'),
    url(r'^map/places/category/(?P<cat_slug>[^/]+)$', 'search_places', name='list_by_category'),
    url(r'map/view/(?P<cat_slug>[^/]+)/(?P<object_id>\d+)$','view', name='view'),
    (r'^map/streets/location$', 'street_location'),
    (r'^tags/(?P<tag>[^/]+)$','obj_list_by_tag'),

)

urlpatterns += patterns( '',
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^acerca_de/', direct_to_template, {'template':'about.html'}),
    (r'^mensajes/', include('messages.urls')),
    (r'^notificaciones/', include('notification.urls')),
    (r"^announcements/", include("announcements.urls")),
    (r'^contacto/$', 'nomenclador.profiles.views.mail', {}, 'mail'),
    )

urlpatterns += patterns('',
    url(r'^activate/complete/$',
       direct_to_template,
       {'template': 'registration/activation_complete.html'},
       name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
       'registration.views.activate',
       {'backend': 'registration.backends.default.DefaultBackend'},
       name='registration_activate'),
    url(r'^register/$',
       'registration.views.register',
       {'backend': 'registration.backends.default.DefaultBackend'},
       name='registration_register'),
    url(r'^register/complete/$',
       direct_to_template,
       {'template': 'registration/registration_complete.html'},
       name='registration_complete'),
    url(r'^register/closed/$',
       direct_to_template,
       {'template': 'registration/registration_closed.html'},
       name='registration_disallowed'),
    (r'', include('registration.auth_urls')),
    (r'^ingresar/$', 'nomenclador.profiles.views.login',{},'login'),
    (r'^salir/$', 'django.contrib.auth.views.logout', {}, 'logout'),
)


#urlpatterns +=(
#    url(r'^registrarse/$', 'registration.signup', name='signup'),
#    url(r'^ingresar/$', 'account.views.login', name='login'),
#)
urlpatterns += patterns('nomenclador',

#    url(r'^miembros/$', 'profiles.views.profiles', name='profile_list'),
    url(r'^miembros/(?P<username>[\w\._-]+)$', 'profiles.views.profile', name='profile_detail'),
    url(r'^miembros/(?P<user_id>[\w\._-]+)/edit$', 'profiles.views.profile_edit', name='profile_edit'),

    )

urlpatterns += patterns( '',

    url(r'^vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, dict(model=MaapModel, 
            template_name='confirm_vote.html',
            allow_xmlhttprequest=True),
        name='vote'),
)
if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    )

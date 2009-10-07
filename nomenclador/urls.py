
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from nomenclador.accounts.forms import MyRegistrationForm
admin.autodiscover()


handler500 # Pyflakes

urlpatterns = patterns( '',
    (r'^$', 'nomenclador.maap.views.index'),
    (r'^admin/(.*)', admin.site.root),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^maap/', include('nomenclador.maap.urls')),
    (r'^accounts/register', 'registration.views.register',{'form_class':MyRegistrationForm}),
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('nomenclador.accounts.urls')),
    (r'^nomtools/', include('nomtools.urls')),
)

if settings.DEBUG:

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )

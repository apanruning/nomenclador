from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('toolsnmt.views',
    # Example:
    (r'^$', 'doors'),
    (r'^nodes_by_street', 'nodes_by_street'),
    (r'^update_nodes', 'update_nodes'),
    (r'^synchronization', 'synchronize_home'),
    (r'^detail_synchronize', 'detail_synchronize'),
    (r'^old_streets', 'old_streets'),
    (r'^old_streets_edit', 'old_streets_edit'),
    (r'^save_last_name', 'save_last_name'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)    
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT}),
    )


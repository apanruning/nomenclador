from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('views',
    # Example:
    (r'^$', 'doors'),
    (r'^tools/doors/', 'doors'),
    (r'^tools/nodes_by_street', 'nodes_by_street'),
    (r'^tools/show_node', 'show_node'),
    (r'^tools/show_street', 'show_street2'),
    (r'^tools/update_nodes', 'update_nodes'),
    (r'^tools/synchronization', 'synchronize_home'),
    (r'^tools/detail_synchronize', 'detail_synchronize'),
    (r'^tools/old_streets', 'old_streets'),
    (r'^tools/old_streets_edit', 'old_streets_edit'),
    (r'^tools/save_last_name', 'save_last_name'),
    
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


from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'profiles.views.profile_list', name='profile_list'),
    url(r'^(?P<username>[\w\._-]+)/$', 'profiles.views.profile', name='profile_detail'),

)

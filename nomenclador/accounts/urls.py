from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^login/$', 'django.contrib.auth.views.login', 
                  {'template_name': 'registration/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout',
                  {'template_name': 'registration/logout.html'}),
    (r'^changepassword/$', 'django.contrib.auth.views.password_change',
                  {'template_name':'registration/password_change_form.html'}),
    (r'^changepassword/done/$', 'django.contrib.auth.views.password_change_done',
                  {'template_name':'registration/password_change_done.html'}),
    url(r'^profile/(?P<username>[^/]+)/$', 'accounts.views.profile'),    
    url(r'^profile/(?P<username>[^/]+)/edit/$', 'accounts.views.edit'),    
# look in django.contrib.auth.views for everything else that should be here
    
)

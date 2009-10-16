from django.conf.urls.defaults import *
from forms import *

urlpatterns = patterns('',
    url(r'^email/$', 'nomenclador.account.views.email', name="acct_email"),
    url(r'^signup/$', 'nomenclador.account.views.signup', name="acct_signup"),
    url(r'^login/$', 'nomenclador.account.views.login', name="acct_login"),
    url(r'^password_change/$', 'nomenclador.account.views.password_change', name="acct_passwd"),
    url(r'^password_set/$', 'nomenclador.account.views.password_set', name="acct_passwd_set"),
    url(r'^password_delete/$', 'nomenclador.account.views.password_delete', name="acct_passwd_delete"),
    url(r'^password_delete/done/$', 'django.views.generic.simple.direct_to_template', {
        "template": "account/password_delete_done.html",
    }, name="acct_passwd_delete_done"),
    url(r'^password_reset/$', 'nomenclador.account.views.password_reset', name="acct_passwd_reset"),
    url(r'^other_services/$', 'nomenclador.account.views.other_services', name="acct_other_services"),
    url(r'^other_services/remove/$', 'nomenclador.account.views.other_services_remove', name="acct_other_services_remove"),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"template_name": "account/logout.html"}, name="acct_logout"),
    
    url(r'^confirm_email/(\w+)/$', 'emailconfirmation.views.confirm_email', name="acct_confirm_email"),

    # Setting the permanent password after getting a key by email
    url(r'^password_reset_key/(\w+)/$', 'nomenclador.account.views.password_reset_from_key', name="acct_passwd_reset_key"),

    # ajax validation
)
urlpatterns += patterns(
(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/path/to/media'}),
)

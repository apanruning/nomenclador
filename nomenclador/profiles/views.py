from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import create_update
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from microblogging.models import Following

from nomenclador.profiles.models import Profile
from nomenclador.profiles.forms import ProfileForm
#from nomenclador.olwidget.widgets import MapDisplay


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def profiles(request, template_name="profiles/profiles.html", extra_context=None):
    if extra_context is None:
        extra_context = {}
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, dict({
        'users': users,
        'order': order,
        'search_terms': search_terms,
    }, **extra_context), context_instance=RequestContext(request))

def profile(request, username, template_name="profiles/profile.html", extra_context=None):
    if extra_context is None:
        extra_context = {}
    other_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        is_following = Following.objects.is_following(request.user, other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        is_me = False
        is_following = False
    
    #display_map = MapDisplay(fields=[other_user.get_profile().location])
    #extra_context = {'map':display_map}
    return render_to_response(template_name, dict({
        "is_me": is_me,
        "is_following": is_following,
        "other_user": other_user,
    }, **extra_context), context_instance=RequestContext(request))
    

@login_required  
def profile_edit(request, user_id):
    return create_update.update_object(
        request, 
        model=Profile, 
        object_id = user_id,
        form_class=ProfileForm, 
        template_name='profiles/profile_form.html')  


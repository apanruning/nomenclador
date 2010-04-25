from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import create_update, simple
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.mail import EmailMessage
from microblogging.models import Following

from nomenclador.profiles.models import Profile
from nomenclador.profiles.forms import ProfileForm, MailForm, InlinePointForm
from nomenclador.maap.models import MaapPoint, Icon
#from nomenclador.olwidget.widgets import MapDisplay


if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

#def profiles(request, template_name="profiles/profiles.html", extra_context=None):
#    if extra_context is None:
#        extra_context = {}
#    users = User.objects.all().order_by("-date_joined")
#    search_terms = request.GET.get('search', '')
#    order = request.GET.get('order')
#    if not order:
#        order = 'date'
#    if search_terms:
#        users = users.filter(username__icontains=search_terms)
#    if order == 'date':
#        users = users.order_by("-date_joined")
#    elif order == 'name':
#        users = users.order_by("username")
#    return render_to_response(template_name, dict({
#        'users': users,
#        'order': order,
#        'search_terms': search_terms,
#    }, **extra_context), context_instance=RequestContext(request))

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

    return render_to_response(template_name, dict({
        "is_me": is_me,
        "is_following": is_following,
        "other_user": other_user,
    }, **extra_context), context_instance=RequestContext(request))
    

@login_required  
def profile_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile_instance = user.get_profile()
    profile_form = ProfileForm(instance = profile_instance)
    default_icon = Icon.objects.get(name='home')
    if profile_instance.location_id is not None:
    
        point = MaapPoint.objects.get(id = profile_instance.location_id)
        import ipdb; ipdb.set_trace()    
        point_form = InlinePointForm(instance = point)
    else:
        point_form = InlinePointForm()
        
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user.get_profile())
        point_form = InlinePointForm(request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            
        if point_form.is_valid():
            point = point_form.save(commit=False)
            point.name = profile.name
            point.creator = User.objects.get(username='admin')
            point.editor = User.objects.get(username='admin')
            point.icon = default_icon

            
        try :
            point.save()
            success = True
        except:
            success = False

        if success:
            profile.user = user            
            profile.location = point
            profile.location_id = point.id
            
        try:
            profile.save()
            success = success and True
        except:
            success = False
            
        if success:
            return redirect('profile_detail', username = user.username)
        
    return simple.direct_to_template(
        request, 
        'profiles/profile_form.html',
        extra_context={
            'form':profile_form,
            'inline_form':point_form,
            'user':user
        }
    )  

def mail(request):
    mailform = MailForm()
    honeypot = request.POST.get('honeypot', None)
    if request.method == 'POST':
        mailform = MailForm(request)
        if mailform.is_valid() and not honeypot:
            data = mailform.cleaned_data
            subject = 'Nuevo mensaje de %s desde la web' %data['name']
            email = EmailMessage(
                subject = data['subject'], 
                body = data['message'],
                from_email = data['email'],
                to = ('info@comercioyjusticia.com',)
                )

            if not settings.DEBUG :                
                email.send()
                    
    return simple.direct_to_template(
        request,
        'contact.html', 
        extra_context={'form':mailform}
    )


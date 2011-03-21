# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import create_update, simple
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.mail import EmailMessage

from profiles.models import Profile
from profiles.forms import ProfileForm, MailForm, InlinePointForm, LoginForm
from maap.models import MaapPoint, Icon
#from olwidget.widgets import MapDisplay


LOGIN_REDIRECT_URLNAME = getattr(settings, "LOGIN_REDIRECT_URLNAME", '')

def get_default_redirect(request, redirect_field_name="next",
        login_redirect_urlname=LOGIN_REDIRECT_URLNAME):
    """
    Returns the URL to be used in login procedures by looking at different
    values in the following order:
    
    - LOGIN_REDIRECT_URLNAME - the name of a URLconf entry in the settings  
    - LOGIN_REDIRECT_URL - the URL in the setting
    - a REQUEST value, GET or POST, named "next" by default.
    """
    if login_redirect_urlname:
        default_redirect_to = reverse(login_redirect_urlname)
    else:
        default_redirect_to = settings.LOGIN_REDIRECT_URL
    redirect_to = request.REQUEST.get(redirect_field_name)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = default_redirect_to
    return redirect_to


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile = user_profile.get_profile()
    if request.user.is_authenticated():
        if request.user == user_profile:
            is_me = True
        else:
            is_me = False
    else:
        is_me = False
    if not profile.name and is_me:
        messages.add_message(
            request, 
            messages.INFO, 
            u'Todavía no ha creado su perfil de usuario'
        )
        return redirect('profile_edit', user_id=user_profile.pk)
    try :
        json_layer = profile.location.to_layer().json
    except:
        json_layer = None
        
    return simple.direct_to_template(
        request,
        'profiles/profile.html', 
        {
        'is_me': is_me,
        'user_profile': user_profile,
        'json_layer': json_layer,
        'created':  user_profile.created.filter(category__isnull=False),
        }
    )

@login_required  
def profile_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile_instance = user.get_profile()
    profile_form = ProfileForm(instance = profile_instance)
    default_icon = Icon.objects.get(name='home')
    if profile_instance.location_id is not None:
        point = MaapPoint.objects.get(id=profile_instance.location_id)
        point_form = InlinePointForm(instance=point)
    else:
        point_form = InlinePointForm()
        point = None
                
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile_instance)
        if point:
            point_form = InlinePointForm(request.POST, instance=point)
        else:
            point_form = point_form(request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            
        if point_form.is_valid():
            point = point_form.save(commit=False)
            point.name = profile.name
            point.creator = request.user
            point.editor = request.user
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


def login(request, success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.login(request):
            return HttpResponseRedirect(success_url)
    else:
        form = LoginForm()
    return simple.direct_to_template(
        request,
        "registration/login.html", 
        extra_context={
        "form": form,
        }
    )


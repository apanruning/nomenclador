from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import SiteUserProfile
from forms import ProfileForm, BaseUserForm
from django.http import Http404

from django.contrib.auth import authenticate, login

        
        
def userprofile(request, username):
    try:
        user = User.objects.get(username__exact=username)
    except User.DoesNotExist:
        raise Http404

    try:
        profile = user.get_profile()
    except SiteUserProfile.DoesNotExist:
        profile = None
        
    if profile:
        context = RequestContext(request, {'profile':profile})
        return render_to_response('registration/profile.html', context_instance=context)    
    else :
        return HttpResponseRedirect(reverse('nomenclador.accounts.views.edit', args=(user.username,)))

def index(request):
    users = User.objects.filter(is_staff=True)
    profiles = []
    for user in users :
        if user.username != 'admin':
            try: 
                profiles.append(user.get_profile())
            except:
                pass
                    
    context = RequestContext(request, {'profiles':profiles})
    return render_to_response('registration/index.html', context_instance=context)

        
@login_required
def edit(request, username):
    """Allows users to edit their profiles """
    try:
        user = User.objects.get(username__exact=username)
    except User.DoesNotExist:
        raise Http404
    
    # check that user is editing your own profile
    if user <> request.user:
        return HttpResponseRedirect("../../login")        
    
    
    try:
        profile = user.get_profile()
    except SiteUserProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        uform = BaseUserForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, request.FILES)
        if pform.is_valid() and uform.is_valid():
            user = uform.save()
            user.save()
            if not profile:
                profile = pform.save(commit=False)
                profile.user = user
                profile.save()
            else:
                pform = ProfileForm(request.POST, request.FILES, instance=profile)
                profile = pform.save()
            
            return HttpResponseRedirect(reverse('accounts.views.profile', args=(user.username,)))
        else:
            context = RequestContext(request, {'userform':uform, 'profileform': pform})
    else:
        uform = BaseUserForm(instance=user)

        if profile:
            pform = ProfileForm(instance=profile)
            context = RequestContext(request, {'userform':uform, 'profileform': pform, 'profile':profile})
        else:
            pform = ProfileForm()
            context = RequestContext(request, {'userform':uform, 'profileform': pform})

    return render_to_response('registration/edit.html', context_instance=context)    


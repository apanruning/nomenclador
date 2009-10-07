from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms as forms

from models import SiteUserProfile
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile

class MyRegistrationForm(RegistrationForm):
    def save(self, profile_callback=None):
        """
        Tuneado parea que sea mas poronga
        """
        
        import pdb
        pdb.set_trace()
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    send_email=False,
                                                                    profile_callback=profile_callback)
        return new_user



class ProfileForm(ModelForm):
    class Meta:
        model = SiteUserProfile
        exclude = ('user')
        

class BaseUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
    
    


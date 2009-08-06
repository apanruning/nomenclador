
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms as forms

from models import SiteUserProfile
from nomenclador.fields import AutoCompleteTagInput, WMDTextField

from tagging.forms import TagField

class ProfileForm(ModelForm):
    class Meta:
        model = SiteUserProfile
        exclude = ('user')
        
    description = forms.CharField(widget=WMDTextField)
    skills = TagField(widget=AutoCompleteTagInput(model=User))

class BaseUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
    
    


from models import SiteUserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms as forms
from wiki.fields import AutoCompleteTagInput, WikiTextField
from tagging.forms import TagField

class ProfileForm(ModelForm):
    class Meta:
        model = SiteUserProfile
        exclude = ('user')
        
    description = forms.CharField(widget=WikiTextField)
    skills = TagField(widget=AutoCompleteTagInput(model=User))

class BaseUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
    
    


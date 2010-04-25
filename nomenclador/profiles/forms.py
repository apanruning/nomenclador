from django import forms
from nomenclador.profiles.models import Profile
from nomenclador.fields import WMDTextField
from nomenclador.maap.models import MaapPoint
from nomenclador.maap.forms import InlinePointForm
from django.forms.models import inlineformset_factory
from django.contrib.gis import admin

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','location')
    description = forms.CharField(widget=WMDTextField, required=False)

class MailForm(forms.Form):
    name = forms.CharField(label = 'Su nombre', max_length = 50)
    mail = forms.EmailField(label = 'Su email')
    message = forms.CharField(label = 'Mensaje', widget=WMDTextField)


from django import forms
from nomenclador.profiles.models import Profile
from nomenclador.fields import WMDTextField

from django.contrib.gis import admin
from nomenclador.maap.admin import GeoCordobaAdmin
#from nomenclador.olwidget.widgets import EditableMap

admin_instance = GeoCordobaAdmin(Profile, admin.site)
point_field = Profile._meta.get_field("location")
PointWidget = admin_instance.get_map_widget(point_field)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'blogrss', 'timezone', 
            'twitter_user', 'twitter_password')
    description = forms.CharField(widget=WMDTextField, required=False)
    location = forms.CharField(widget=PointWidget, required=False)
  

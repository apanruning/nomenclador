from django import forms
from nomenclador.maap.admin import GeoCordobaAdmin
from nomenclador.maap.models import MaapPoint
from django.contrib.gis import admin

admin_instance = GeoCordobaAdmin(MaapPoint, admin.site)
point_field = MaapPoint._meta.get_field("geom")
PointWidget = admin_instance.get_map_widget(point_field)

class InlinePointForm (forms.ModelForm):
    geom = forms.CharField(widget=PointWidget, required=False)
    class Meta:
        model = MaapPoint
        exclude = (
            'slug', 
            'description', 
            'default_layers', 
            'metadata', 
            'category', 
            'tags',
            'banner_slots',
            'name',
            'icon',
         )
    

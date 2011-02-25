# -*- coding: utf-8 -*-
from maap.admin import GeoCordobaAdmin
from maap.models import MaapPoint
from django.contrib.gis import forms, admin

admin_instance = GeoCordobaAdmin(MaapPoint, admin.site)
point_field = MaapPoint._meta.get_field("geom")
PointWidget = admin_instance.get_map_widget(point_field)

class InlinePointForm (forms.ModelForm):
    geom = forms.CharField( label=u'Dirección', widget=PointWidget, required=False)
    class Meta:
        model = MaapPoint
        exclude = (
            'slug', 
            'description', 
            'default_layers', 
            'metadata', 
            'category', 
            'tags',
            'popup_text',
            'closest',
            'banner_slots',
            'name',
            'icon',
         )
    
class MaapPointForm(forms.ModelForm):
    geom = forms.CharField(label='Dirección', widget=PointWidget, required=True)
    class Meta:
        model = MaapPoint
        exclude = (
            'default_layers',
            'metadata',
            'popup_text',
            'icon',
            'tags',
            'closest',
            'banner_slots',
        )
        
    def save(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()

        if not self.instance.creator_id:
            self.instance.creator_id = self.data['user']

        self.instance.editor_id = self.data['user']
        return super(forms.ModelForm, self).save(*args, **kwargs)

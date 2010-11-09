from django import forms

import re

from django.db.models import get_model
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag

from django.conf import settings

  
class AutoCompleteTagInput(forms.TextInput):
    def __init__(self, model=None, attrs=None):        
        obj_tags = Tag.objects.usage_for_model(model)
        self.tag_list = simplejson.dumps([tag.name for tag in obj_tags],
                                    ensure_ascii=False)
    
        super(AutoCompleteTagInput, self).__init__(attrs)           

    class Media:
        css = {
            'all': ('/media/css/jquery.autocomplete.css',)
        }
        js = (
            '/media/js/jquery.ajaxQueue.js',
            '/media/js/jquery.autocomplete.js'
        )
    def render(self, name, value, attrs=None):
        attrs.update({'style':'width:250px'})
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)

        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 250,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, self.tag_list))
            
            


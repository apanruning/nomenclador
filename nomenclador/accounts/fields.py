from django import forms

import re

from django.db.models import get_model
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag

from django.conf import settings

       
class WMDTextField(forms.Textarea):
    class Media:
        css = {
            'all': ('/accounts/media/wmd.css',)
        }
        js = (
            '/accounts/media/showdown.js',
            '/accounts/media/jquery.textarearesizer.js'

        )  

    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        if 'id' not in attrs:
            attrs['id'] = 'wmd-input'
        if 'cols' not in attrs:
            attrs['cols'] = 112
        if 'rows' not in attrs:
            attrs['rows'] = 12
        super(WMDTextField, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        rendered = super(WMDTextField, self).render(name, value, attrs)
        
        return mark_safe(u'''
             <div id="wmd-field">
                  <div id="wmd-button-bar" class="wmd-panel"></div>

                  %s  

                  <div id="wmd-preview" class="wmd-panel"></div>
                  <div id="wmd-output" class="wmd-panel"></div>	
                  <script type="text/javascript">
                    wmd_options = {
                        output: "Markdown",
                        buttons: "bold italic | link blockquote code image | ol ul"
                    };
                  </script>
                  <script type="text/javascript" src="/accounts/media/wmd.js"></script>      
              </div>
            ''' %rendered )

  
class AutoCompleteTagInput(forms.TextInput):
    def __init__(self, model=None, attrs=None):        
        obj_tags = Tag.objects.usage_for_model(model)
        self.tag_list = simplejson.dumps([tag.name for tag in obj_tags],
                                    ensure_ascii=False)
    
        super(AutoCompleteTagInput, self).__init__(attrs)           

    class Media:
        css = {
            'all': ('/accounts/media/jquery.autocomplete.css',)
        }
        js = (
            '/accounts/media/jquery.ajaxQueue.js',
            '/accounts/media/jquery.autocomplete.js'
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
            
            


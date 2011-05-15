from django.contrib.gis import admin
from models import *
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import  get_object_or_404
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django import template
from copy import deepcopy
from django.conf import settings

class MpttAdmin(admin.ModelAdmin):
    """ Base class for mptt model admins, usage:
        class ExampleAdmin(MpttAdmin):
            tree_title_field = 'name'
            tree_display = ('name','slug','created|date') # you can use filters here
            prepopulated_fields = {"slug": ("name",)}
            class Meta:
                model = Example
    """
    def __init__(self,*args,**kargs):
        super(MpttAdmin,self).__init__(*args,**kargs)
        if not hasattr(self,'tree_display'):
            self.tree_display = ()
        if self.tree_display and not hasattr(self,'tree_title_field'):
            self.tree_title_field = self.tree_display[0]
        if not hasattr(self,'tree_title_field'):
            title_field = ''#self.tree_display[0]
        else:
            title_field = '.'+self.tree_title_field
        extra_fields = '&nbsp;'.join('<span title="%s">{{ node.%s }}</span>' % (field,field) for field in self.tree_display if not hasattr(self,'tree_title_field') or field!=self.tree_title_field)
        model = '%s.%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.object_name)
        self._tree_tpl = template.Template("""{% load mptt_tags %}{% full_tree_for_model """+model+""" as nodes %}{% for node,structure in nodes|tree_info %}{% if structure.new_level %}{% if node.is_child_node %}<ul>{% endif %}<li id="n{{node.pk}}">{% else %}</li><li id="n{{node.pk}}">{% endif %}<ins> </ins><a href="{{node.pk}}/">{{ node"""+title_field+""" }}</a>"""+extra_fields+"""{% for level in structure.closed_levels %}</li>{% if node.is_child_node %}</ul>{% endif %}{% endfor %}{% endfor %}""")
        self._changelist_tpl = template.Template("""{% extends "admin/change_list.html" %}
        {% load mptt_tags %}        
        {% block extrahead %}
        <script>var permissions={{permissions|safe}};</script>
        <script src="{{ settings.MEDIA_URL }}js/jstree_admin.js"></script>
        {% endblock %}
        {% block search %}{% endblock %}{% block date_hierarchy %}{% endblock %}
        {% block result_list %}{% endblock %}{% block pagination %}{% endblock %}
        {% block filters %}<div id="tree"><ul>{{tree}}</ul></div>{% endblock %}""")

        #self.move_node = permission_required('%s.change_%s' % (self.model._meta.app_label,self.model._meta.object_name))(self.move_node)
        #self.rename = permission_required('%s.change_%s' % (self.model._meta.app_label,self.model._meta.object_name))(self.rename)
        #self.remove = permission_required('%s.delete_%s' % (self.model._meta.app_label,self.model._meta.object_name))(self.remove)

    def changelist_view(self, request, extra_context=None):
        model = '%s.%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.object_name)
        opts = self.model._meta
        app_label = opts.app_label

        media = deepcopy(self.media)
        media.add_js(['jquery.min.js',
            'js/lib/jquery.tree.min.js',
            'js/lib/plugins/jquery.tree.contextmenu.js'])

        module_name = force_unicode(opts.verbose_name_plural)

        permissions = simplejson.dumps({
            'renameable' : self.has_change_permission(request, None) and hasattr(self,'tree_title_field'),
		    'deletable'	: self.has_delete_permission(request, None),
		    'creatable'	: self.has_add_permission(request),
		    'draggable'	: self.has_change_permission(request, None),
        })

        context = {
            'module_name': module_name,
            'title': module_name,
            'is_popup': False,
            'cl': {'opts':{'verbose_name_plural': module_name}},
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'root_path': self.admin_site.root_path,
            'app_label': app_label,
            'tree':self._tree_tpl.render(template.Context()),
            'permissions': permissions,
            'settings.MEDIA_URL': settings.settings.MEDIA_URL,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        context_instance.update(context)
        return HttpResponse(self._changelist_tpl.render(context_instance))

    def get_urls(self):
        urls = super(MpttAdmin, self).get_urls()

        my_urls = patterns('',
            (r'^tree/$', self.get_tree),
            (r'^move_node/$', self.move_node),
            (r'^rename/$', self.rename),
            (r'^remove/$', self.remove),
        )
        return my_urls + urls

    def get_tree(self,request):
        return HttpResponse(self._tree_tpl.render(template.Context()))

    def move_node(self,request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        target = get_object_or_404(self.Meta.model,pk=request.POST.get('target'))
        position = request.POST.get('position')
        if position not in ('left','right','last-child','first-child'):
            return HttpResponseBadRequest('bad position')
        self.Meta.model.tree.move_node(node,target,position)
        return self.get_tree(request)

    def rename(self,request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        setattr(node,self.tree_title_field, request.POST.get('name'))
        print self.tree_title_field, request.POST.get('name')
        node.save()
        return self.get_tree(request)

    def remove(self,request):
        if not self.has_delete_permission(request, None):
            raise PermissionDenied
        node = get_object_or_404(self.Meta.model,pk=request.POST.get('node'))
        node.delete()
        return self.get_tree(request)


class MaapCategoryAdmin(MpttAdmin):
    #tree_title_field = 'maapcategory'
    tree_display = ('name',) # you can use filters here
    #prepopulated_fields = {"slug": ("name",)}
    class Meta:
        model = MaapCategory

class GeoCordobaAdmin(admin.OSMGeoAdmin):
    default_lat = -3686022.8143382
    default_lon = -7145792.0249884
    #display_wkt = True
    default_zoom = 12
    map_width = 800
    map_height = 600
    
    extra_js =[settings.MEDIA_URL+'js/OpenStreetMap.js',
               settings.MEDIA_URL+'js/jquery.min.js', 
               settings.MEDIA_URL+'js/tiny_mce/tiny_mce.js',
               settings.MEDIA_URL+'js/tiny_mce/jquery.tinymce.js',
               settings.MEDIA_URL+'js/tiny_mce/textareas.js',]
    
    list_display = ('name','creator','created')           
    list_filter = ('creator','category','created')
    ordering = ('created','creator','category')
    search_fields = ('creator','created','creator')

    def save_model(self, request, obj, form, change):

        obj.editor = request.user
        if not change:
            obj.creator = request.user
        obj.save()
        
   
admin.site.register(MaapCategory, MaapCategoryAdmin)
admin.site.register(MaapPoint, GeoCordobaAdmin)
admin.site.register(Icon, admin.GeoModelAdmin)
admin.site.register(MaapZone, GeoCordobaAdmin)
admin.site.register(MaapArea, GeoCordobaAdmin)
admin.site.register(MaapMultiLine, GeoCordobaAdmin)


from django import template
from maap.models import MaapCategory, MaapModel
from django.utils.http import urlencode
from django.template.defaultfilters import slugify

register = template.Library()

@register.inclusion_tag('../templates/category_list.html')
def category_list(current_node = None, searchterm = None):
    if not current_node:
        roots = MaapCategory.tree.root_nodes()
    else:
        roots = current_node.get_children()
        
    out = dict(roots = roots, current = current_node)
    if searchterm:
        out['param'] = "?searchterm=%s" % searchterm
        
    return out
    
@register.inclusion_tag('../templates/barrios.html')
def neighbour_list(current_node = None):
    return dict(object_list = MaapModel.objects.filter(category__name='Barrios'))
    
@register.inclusion_tag('../templates/breadcrumbs.html')
def breadcrumbs(current_node = None):
    return dict(current = current_node)

@register.inclusion_tag('../templates/suggested_categories.html')
def suggested_categories(search_term = None):
    categories = MaapCategory.objects.filter(slug__contains = slugify(search_term))[:5]
    
    return dict(categories = categories)

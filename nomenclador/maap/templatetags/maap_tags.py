from django import template
from nomenclador.maap.models import MaapCategory
from django.utils.http import urlencode

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

@register.inclusion_tag('../templates/breadcrumbs.html')
def breadcrumbs(current_node = None):
    return dict(current = current_node)


from django import template
import urllib, hashlib

register = template.Library()

def show_profile(user):
    return {"user": user}
register.inclusion_tag("profile_item.html")(show_profile)

def clear_search_url(request):
    getvars = request.GET.copy()
    if 'search' in getvars:
        del getvars['search']
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path
register.simple_tag(clear_search_url)


@register.simple_tag
def gravatar(email, size=48):
    """
    Simply gets the Gravatar for the commenter. There is no rating or
    custom "not found" icon yet. Used with the Django comments.
    
    If no size is given, the default is 48 pixels by 48 pixels.
    
    Template Syntax::
    
        {% gravatar comment.user_email [size] %}
        
    Example usage::
        
        {% gravatar comment.user_email 48 %}
    
    """
    
    url = "http://www.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(), 
        'size': str(size)
    })
    
    return """<img src="%s" width="%s" height="%s" alt="gravatar" class="gravatar" border="0" />""" % (url, size, size)


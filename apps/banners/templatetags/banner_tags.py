from django import template
from banners.models import Banner
from random import choice
register = template.Library()

@register.inclusion_tag('slot.html')
def pop_slot(slot):
    banner=None
    try :
        banners = Banner.objects.filter(slot=slot)
    except Banner.DoesNotExists:
        banners=None
    if banners:
        banner = choice(banners)
    return {'banner':banner}
    
@register.inclusion_tag('../templates/slot.html')
def lookup_banners(slot):
    try :
        banners = Banner.objects.filter(slot__contains=slot)
    except Banner.DoesNotExists:
        banners=None
    return {'banners':banners}

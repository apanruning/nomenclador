from django import template
from banners.models import Banner

register = template.Library()

@register.inclusion_tag('../templates/slot.html')
def pop_slot(slot):
    try :
        banners = Banner.objects.filter(slot=slot)
    except Banner.DoesNotExists:
        banners=None
    return {'banners':banners}
    

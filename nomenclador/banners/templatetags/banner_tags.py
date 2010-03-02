from django import template
from nomenclador.banners.models import Banner

register = template.Library()

@register.inclusion_tag('../templates/slot.html')
def pop_slot(slot):
    try :
        banners = Banner.objects.filter(slot=slot)
    except Banner.DoesNotExists:
        banners=None
    return {'banners':banners}
    
@register.inclusion_tag('../templates/slot.html')
def lookup_banners(slot):
    try :
        banners = Banner.objects.filter(slot__contains=slot)
    except Banner.DoesNotExists:
        banners=None
    return {'banners':banners}

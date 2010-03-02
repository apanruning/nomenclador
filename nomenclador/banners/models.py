from django.db import models
from tagging.fields import TagField

class Banner(models.Model):
    image = models.ImageField(upload_to='banners', blank=True)
    url = models.URLField(blank=True)
    code = models.TextField(blank=True)
    slot = TagField()
    clicks = models.PositiveIntegerField(default=0, blank=True)
    views = models.PositiveIntegerField(default=0, blank=True)
    def __unicode__(self):
        return "Banner #%s on %s" %(self.pk, self.slot)
    
    
    

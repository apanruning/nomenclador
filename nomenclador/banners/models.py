from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners', blank=True)
    url = models.URLField(blank=True)
    code = models.TextField(blank=True)
    slot = models.CharField(max_length=50)
    clicks = models.PositiveIntegerField(default=0, blank=True)
    views = models.PositiveIntegerField(default=0, blank=True)
    
    
    

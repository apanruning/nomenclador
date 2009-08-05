from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners')
    url = models.URLField()
    slot = models.CharField(max_length=50)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    
    
    

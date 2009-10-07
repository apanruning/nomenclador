from django.db import models
from django.contrib.auth.models import User

class SiteUserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='images', blank= True)
    public_profile = models.BooleanField()
    class Meta:
        verbose_name = (u'Perfil de usuario')
        verbose_name_plural = (u'Perfiles de usuarios')
            
    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)



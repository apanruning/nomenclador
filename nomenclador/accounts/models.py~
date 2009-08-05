from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _

class SiteUserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='images', blank= True)
    skills = TagField(blank=True)
    hours_per_week = models.SmallIntegerField()
    @property
    def capacity(self):
        raise NotImplementedError

    class Meta:
        verbose_name = _(u'User Profile')
        verbose_name_plural = _(u'User Profiles')
        permissions = (
            ('view', 'Can view the user stories.'),
        )
            
    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):

        super(SiteUserProfile, self).save(*args, **kwargs)


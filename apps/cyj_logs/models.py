from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger('searchlog')

LOG_LEVELS = (
    (logging.INFO, _('info')),
    (logging.WARNING, _('warning')),
    (logging.DEBUG, _('debug')),
    (logging.ERROR, _('error')),
    (logging.FATAL, _('fatal')),
)

class SearchLog(models.Model):
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable = False)
    url = models.URLField(verify_exists=False, null=True, blank=True)
    level = models.PositiveIntegerField(choices=LOG_LEVELS, default=logging.ERROR, blank=True)

    

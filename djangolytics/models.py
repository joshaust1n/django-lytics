from django.db import models
from django.conf import settings
from django.utils import timezone

class EventModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    when = models.DateTimeField(default=timezone.now, null=False, blank=False)
    ip   = models.GenericIPAddressField(null=False, blank=False)
    tag  = models.TextField(null=False, blank=False)
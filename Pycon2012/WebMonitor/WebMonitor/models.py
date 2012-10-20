from django.db import models
from datetime import datetime


class Monitor(models.Model):
    """ This contains all the monitored parameter """
    url = models.URLField(max_length=50)    #url
    httpStatus = models.CharField(max_length=20)    #http status
    responseTime = models.CharField(max_length=20)    #response time
    contentStatus = models.BooleanField()               #content state
    created_at = models.DateTimeField(default=datetime.now(),blank=True,editable=False)

    class Meta:
        ordering = ['-created_at']







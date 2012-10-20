from django.db import models
from YAAS.models import CustomUser, Item

class Message(models.Model):
    text = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(CustomUser, blank=True, db_index=True, null=True)
    item = models.ForeignKey(Item, blank=True, null=True, db_index=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.text

from django.db import models


class SearchTerm(models.Model):
    """ stores the text of each internal search submitted """
    q = models.CharField(max_length=50)
    search_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()

    
    def __unicode__(self):
        return self.q

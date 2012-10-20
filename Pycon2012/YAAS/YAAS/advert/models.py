from django.db import models
from YAAS import extra
from datetime import datetime
from YAAS.extra import ContentTypeRestrictedFileField


def get_image_path(instance, filename):
    return 'adverts/%s_%s' % (extra.createRandom(), filename)



#This customizes the item to show only visible adverts
class ActiveAdvertManager(models.Manager):
	def get_query_set(self):
		return super(ActiveAdvertManager, self).get_query_set().filter(visibility=True)

class Advertisement(models.Model):
	name = models.CharField(max_length=30, help_text='Enter the name of the advert')
	description = models.CharField(max_length=150, help_text='Enter the description of the advert')
	visibility = models.BooleanField(default = True) 
	created_at = models.DateTimeField(default=datetime.now(),blank=True,editable=False)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)

	image = ContentTypeRestrictedFileField(
        upload_to=get_image_path,
        content_types=['image/pjpeg' , 'image/jpeg','image/tiff','image/png','image/gif'],
        max_upload_size=2.5*1024*1024,
		blank=True,
		null=True
    )

	objects = models.Manager()
	active = ActiveAdvertManager()
	class Meta:
		ordering = ['-created_at']  

	def __unicode__(self):
		return self.name 


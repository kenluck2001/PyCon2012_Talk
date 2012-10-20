from django.contrib.auth.models import User , UserManager # UserManager
from django.db import models
from YAAS import extra
from YAAS.extra import ContentTypeRestrictedFileField
from datetime import datetime, timedelta
from YAAS.customerReview.models import ProductReview


def get_image_path(instance, filename):
    return 'pictures/%s_%s' % (extra.createRandom(), filename)



class CustomUser(User):
	"""User with app settings."""
	STATUS_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	created_at = models.DateTimeField(default=datetime.now(),blank=True, editable=False)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)
	activation_key = models.CharField(null=True , blank=True, max_length=50)
	keyexpiry_date = models.DateTimeField(null=True , blank=True )
	phone_number = models.CharField(max_length=50)
	sex = models.CharField(max_length=1, choices=STATUS_CHOICES)

	#Use UserManger to get the create_user method, etc.
	objects = UserManager()


#This customizes the item to show only visible items
class ActiveItemManager(models.Manager):
	def get_query_set(self):
		return super(ActiveItemManager, self).get_query_set().filter(status=True)

#This can be alternatively called auctions
class Item(models.Model):
	'''
	True 	visible
	False 	invisible
	'''
	owner = models.ForeignKey(CustomUser, db_index=True)
	name = models.CharField(max_length=30, help_text='Enter the name of the item', db_index=True)
	description = models.CharField(max_length=150,help_text='Enter the description of the item', db_index=True)
	minimum_price = models.DecimalField(max_digits=9,decimal_places=2, default=0.00)
	highestbid = models.DecimalField(max_digits=9,decimal_places=2, default=0.00)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(default=datetime.now(),blank=True,editable=False)
	updated_at = models.DateTimeField(auto_now_add=True, blank=True)
	end_date = models.DateTimeField( default=datetime.now()+timedelta(days=3) )
	image = ContentTypeRestrictedFileField(
        upload_to=get_image_path,
        content_types=['image/pjpeg' , 'image/jpeg','image/tiff','image/png','image/gif'],
        max_upload_size=2.5*1024*1024,
		blank=True,
		null=True
    )

	objects = models.Manager()
	active = ActiveItemManager()
	class Meta:
		ordering = ['-created_at']

	def __unicode__(self):
		return self.name


	#make bid
	@models.permalink
	def get_absolute_url(self):
		return ('YAAS.views.makebid', [str(self.id)])

 
#This customizes the item to show only visible items
class ActiveBidManager(models.Manager):
	def get_query_set(self):
		return super(ActiveBidManager, self).get_query_set().filter(bid_status=False).filter(availability=True)

class Bid(models.Model):
	'''
			#bid_status
			#False 	waiting 
			#True 	resolved

			#payment_status
			#False 	not paid
			#True 	paid

			#availability :needed during maintenance
			#False 	invisible
			#True 	visible
	'''
	user = models.ForeignKey(CustomUser, db_index=True)
	item = models.ForeignKey(Item, db_index=True)
	review = models.ForeignKey(ProductReview, null=True, db_index=True)
	bid_status = models.BooleanField(default = False) 
	bid_price = models.DecimalField(max_digits=9,decimal_places=2, default=0.01)
	availability = models.BooleanField(default = True) 
	created_at = models.DateTimeField(default=datetime.now(),blank=True)
	is_winner = models.BooleanField(default = False) 
	is_emailed = models.BooleanField(default = False) 
	objects = models.Manager()
	active = ActiveBidManager()
	class Meta:
		ordering = ['-bid_price' , '-created_at']   



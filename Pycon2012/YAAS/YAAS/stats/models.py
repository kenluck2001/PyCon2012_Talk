from django.db import models
from datetime import datetime


class RegisteredUser(models.Model):
	no_of_reg_user = models.IntegerField(default=0)
	day = models.IntegerField(default=0)
	month= models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	week= models.IntegerField(default=0)

class OnlineUser(models.Model):
	no_of_online_user = models.IntegerField(default=0)
	day = models.IntegerField(default=0)
	month= models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	week = models.IntegerField(default=0)
	time_of_event = models.DateTimeField(default=datetime.now(),blank=True, editable=False)

class StatBid(models.Model):
	no_of_bids = models.IntegerField(default=0)
	day = models.IntegerField(default=0)
	month= models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	week= models.IntegerField(default=0)

#This work is licensed under the Creative Commons Attribution-Share Alike 3.0 License.
#To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0

#Written by Abd Allah Diab (mpcabd)
#Email: mpcabd ^at^ gmail ^dot^ com
#Website: http://magicpc.wordpress.com

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserActivity(models.Model):
    last_activity_ip = models.IPAddressField()
    last_activity_date = models.DateTimeField(default = datetime(1950, 1, 1))
    user = models.OneToOneField(User, primary_key=True)
#This work is licensed under the Creative Commons Attribution-Share Alike 3.0 License.
#To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0

#Written by Abd Allah Diab (mpcabd)
#Email: mpcabd ^at^ gmail ^dot^ com
#Website: http://magicpc.wordpress.com

from models import UserActivity
from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
import re

compiledLists = {}

class LastActivityMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        urlsModule = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        skipList = getattr(urlsModule, 'skip_last_activity_date', None)
        skippedPath = request.path
        if skippedPath.startswith('/'):
            skippedPath = skippedPath[1:]
        if skipList is not None:
            for expression in skipList:
                compiledVersion = None
                if not compiledLists.has_key(expression):
                    compiledLists[expression] = re.compile(expression)
                compiledVersion = compiledLists[expression]
                if compiledVersion.search(skippedPath):
                    return
        
        activity = None
        try:
            activity = request.user.useractivity
        except:
            activity = UserActivity()
            activity.user = request.user
            activity.last_activity_date = datetime.now()
            activity.last_activity_ip = request.META['REMOTE_ADDR']
            activity.save()
            return
        activity.last_activity_date = datetime.now()
        activity.last_activity_ip = request.META['REMOTE_ADDR']
        activity.save()
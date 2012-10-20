from HTTPClass import HTTPClass

from WebMonitor.models import Monitor

from django.template import RequestContext, Context,  loader
from celery.task.schedules import crontab  
from celery.decorators import periodic_task 
from django.shortcuts import get_object_or_404
from WebMonitor import settings


class LoadEvent:	

    def __init__(self , xmlFileName = "config.xml"):
        self.myhttp = HTTPClass(xmlFileName) #create the HTTP  object
        self.monitorObjList = self.myhttp.checkedContent() #get complete response object

    def fillMonitorModel(self):
        for monObj in self.monitorObjList:
            mObj = Monitor(url = monObj[2], httpStatus = monObj[0], responseTime = monObj[1], contentStatus = monObj[5])
            mObj.save()

    def logEvents(self, filename = "logFolder/log.txt"):
        #save content of monitorObjList to a log file
        logfile = open(filename, 'a')      #append the file to prevent overwriting   
        for monObj in self.monitorObjList:
            #write to file in the order of url, httpStatus, responseTime, currrent time stamp , contentStatus
            wordString = "{0} | {1} | {2} | {3} | {4}\n".format(monObj[2], monObj[0], monObj[1], monObj[4],  self.__setyesNo(monObj[5]))
            logfile.write(wordString)
        logfile.close() 

    def __setyesNo(self, value):
        if value: 
            return 'Yes'
        else: 
            return 'No'

          
@periodic_task(run_every=crontab(hour=settings.HOUR, minute=settings.MINUTE, day_of_week=settings.DAY_OF_WEEK))  
def PerformCheck():
    event = LoadEvent()
    event.fillMonitorModel()
    event.logEvents()

    

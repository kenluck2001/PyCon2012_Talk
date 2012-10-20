from django.utils import unittest
from WebMonitor.models import Monitor
import os
import requests


class TestMonitor(unittest.TestCase):
    """
    A test class for the Monitor module.
    """

    def setUp(self):
        self.monitorObj = Monitor.objects.all()

    def testIfDatabaseIsLoaded(self):
        """check if the database is loaded"""
        number_of_records = self.monitorObj.count()
        self.assertEqual(number_of_records, 0)

    def testLogFileSize(self):
        """ check if entry have been logged in the log file.
            check for file size
        """
        fileSize = self.__getFileSize()
        self.assertEqual(fileSize, 0)

    def testMonitorDataURL(self):
        """ check for generated url of monitor statistics """
        url = "http://127.0.0.1:8080/monitor/" 
        res = requests.get(url)
        self.assertEqual(res.status_code, requests.codes.ok)


    def __getFileSize(self, filename = "logFolder/log.txt"):
        """ Get the size of the log file """
        currentDirectory = os.getcwd()
        filePath = currentDirectory + "/" + filename
        fileSize = os.path.getsize(filePath)
        return fileSize 


from Configuration import Configuration
import test
import time
import requests
from datetime import datetime
import requests  #library for HTTP
import lxml.html  #library for parsing HTML


class HTTPClass:

    def __init__(self, xmlFileName = "config.xml"):
        """ Initializes the Cofiguration class """
        self.conf = Configuration(xmlFileName) #create the configuration object

    def getResponses(self):
        """ get all the response object attributes in a suitable structure """
        propertyList = []
        url_content = self.conf.MapUrlToContent()

        for url, content in url_content:
            start_time = time.time()
            #create a Response object //remove all the required attributes to be logged

            try:
                res = requests.get(url)     #make a get request to know status code
                final_time = time.time()
                real_time = final_time - start_time #duration of request
                #get Http response status
                resStatus = self.__getResponseStatus(res)
                output = resStatus,real_time, url , content, self.__getCurrentTime() #response object, duration, url, content, current time 
                propertyList.append(output)
            except ValueError:
                print "This Url is not valid: ", url
            except ConnectionError: 
                print "DNS failure, refused connection"
            except HTTPError:
                print "Invalid HTTP response"  
            except TooManyRedirects:
                print "Exceeds the configured number of maximum redirections"

        return propertyList

    def __getCurrentTime(self): #make method private
        return str(datetime.now())

    def __getResponseStatus(self, res):
        """ This gets the status """
        status = None 
        if res.status_code == requests.codes.ok:
            status = "Success"

        if res.status_code == 404:
            #Not Found
            status = "Not Found"
        if res.status_code == 408:
            #Request Timeout
            status = "Request Timeout"
        if res.status_code == 410:
            #Gone no longer in server
            status = "Not ON Server"

        if res.status_code == 503:
            #Website is temporary unavailable for maintenance
            status = "Temporary Unavailable"
        if res.status_code == 505:
            #HTTP version not supported
            status = "HTTP version not supported"

        return status

    def getCheckingPeriod(self):
        return self.conf.getCheckingPeriod()

    def numberOfWebSites(self):
        return self.conf.numberOfWebSites()

    def __getPageTitleFromUrl(self, url):
        """let us the title text as the content for comparison. This because it is less updated. We need a variable that is not always changed when making comparisons."""
        t = lxml.html.parse(url)
        return t.find(".//title").text


    def checkedContent(self):
        """url , content variable is the second and third index respectively in the response object tuple
           Append a true or false to specify if a match is found or not
           This is a more complete structure of the response object that can be saved in the database in one pass
        """
        outputList = []
        responseList = self.getResponses()
        for responseObj in responseList:
            #print responseObj #tuple
            url =  responseObj[2] ; content = responseObj[3]
            webContent = self.__getPageTitleFromUrl(url)  #get web page using the Url
            #compare the content of the web page to the content save in the configuration file
            #convert response object to list
            responseList = list(responseObj)
            if self.__processString(webContent) == self.__processString(content) :
                # A match is found
                responseList.append(True)
            else:
                #A match is not found
                responseList.append(False)
            outputList.append(responseList)
        return outputList



    def __processString(self,text):
        #removes all the spaces and convert to lower case
        return text.replace(" ", "").lower()


if __name__ == '__main__' :
    #xmlFileName = "config.xml"
    myhttp = HTTPClass()
    print myhttp.checkedContent()[0]
        


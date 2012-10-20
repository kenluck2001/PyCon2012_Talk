from xml.dom.minidom import parse, parseString
import os



class Configuration:
    """ Handles all the configuration from XML file """

    def __init__(self, xmlFileName = "config.xml"):
        """ get the file and initializes the XML document """
        currentDirectory = os.getcwd()
        xmlFilePath = currentDirectory + "/" + xmlFileName
        datasource = open(xmlFilePath)
        xmldoc = parse(datasource)   # parse an open file
        self.root  = xmldoc.documentElement  #root element

    def getText(self, element):
        my_n_node = element[0]
        my_child = my_n_node.firstChild
        my_text = my_child.data 
        return my_text


    def MapUrlToContent(self):
        """ Create a mapping of url to content """
        outputList = []
        for nod in self.root.getElementsByTagName("Website"):
            urlElement = nod.getElementsByTagName("Url")
            contentElement = nod.getElementsByTagName("Content")
            ##print getText(urlElement), getText(contentElement)
            value = str(self.getText(urlElement)), str(self.getText(contentElement)) #gets a tuple
            outputList.append(value)  
        return outputList

    def getCheckingPeriod(self):
        """ gets the checking period saved in the configuarion file"""
        time = self.root.getElementsByTagName("Time")
        output = None
        for timeObj in time:
            hourElement = timeObj.getElementsByTagName("Hour")
            minuteElement = timeObj.getElementsByTagName("Minute")
            dayOfWeekElement = timeObj.getElementsByTagName("Day_Of_Week")
            output = str(self.getText(hourElement)), str(self.getText(minuteElement)), str(self.getText(dayOfWeekElement))
        return output

    def numberOfWebSites(self):
        #returns the number of website tags
        count = 0
        for nod in self.root.getElementsByTagName("Website"):
            count = count + 1
        return count

if __name__ == '__main__' :
    #xmlFileName = "config.xml"
    myConf = Configuration()
    #print  myConf.MapUrlToContent()
    #print myConf.getCheckingPeriod()
    print myConf.numberOfWebSites()



    








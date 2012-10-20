Target OS:      Ubuntu 11.04
Python version: python 2.7 

Third party libraries
----------------------
Django 1.3  :This is the version of the Django web framework.

Python 2.7  :This is the version of python used in this project.

MySQL 5.1   :This is the version of relational database used in this project.

Firefox 5.0.1   :A modern open source web browser.

django-celery   :This is a free asynchronous task queue/job queue based on
distributed message passing.

ghetto          :This is a queue framework and it works with django-celery.

django-picklefield  :This is implementation of a pickled object field. This works with Django-celery and Ghettoq.

django-kombu        :This works with Django-celery, Ghettoq picklefield. This serves as a message store.

pip     : for installing

requests: for handling HTTP

django-unittest-depth: for unit testing

lxml: for parsing XML



How to set up the system
--------------------------
use pip
* install pip
sudo apt-get install python-pip

* install requests library
* Download binary from the repository and install them in place
sudo pip install -i http://pip.kennethreitz.com/simple requests

* Install gevent for asynchronous connection
Installing Gevent
sudo apt-get install libevent-dev

* Install lxml for parsing HTML
sudo apt-get install python-lxml

* Install webbrowser module. It is already available in python2.7 standard library.

* Download Django binary from the https://www.djangoproject.com/download/
unpack to a suitable directory.
Navigate to bin directory

* Install mysql backend
sudo apt-install mysql-server
sudo apt-get install python-mysqldb

* Install mysql backend to communicate with django
sudo apt-get install python-setuptools
sudo python setup.py install

To start a new project
Django-1.3.1/django/bin$ django-admin.py startproject WebMonitor

* Install mysql
log into your mysql account
mysql -u root -p: enter password

* Install django-unittest-depth
sudo easy_install django-unittest-depth


Then create a database

CREATE DATABASE WebMonitor CHARACTER SET utf8;
CREATE USER 'ken'@'localhost' IDENTIFIED BY 'pass';
GRANT ALL ON WebMonitor.* TO 'ken'@'localhost';


To run django server
python manage.py runserver 8080

To syncronize the database
python manage.py syncdb



To abstract crontab to look like a scheduler is written in pure python. We have to download and install the following packages.

I prefer to use easy_install instead of pip

django-celery       (http://packages.python.org/django-celery/ )
ghettoq             (http://pypi.python.org/pypi/ghettoq )
django-picklefield  (http://pypi.python.org/pypi/django-picklefield )
django-kombu        (https://github.com/ask/django-kombu#readme )
django-unittest-depth   (http://pypi.python.org/pypi/django-unittest-depth/0.6#downloads)


To activate the crontab abstraction for events. We have to 
a)Start a Celery worker
Navigate to folder in your directory that contains the manage.py file. The run the python script as shown below
$ python manage.py celeryd --verbosity=2 --loglevel=DEBUG 

b) Start celerybeat to periodically send registered tasks to ghettoq:
$ python manage.py celerybeat --verbosity=2 --loglevel=DEBUG 

Make sure that these two command are run in seperate command prompt windows.


After setup is successful. We have to run the server to see our work.
Navigate to the directory where manage.py file exist and run this command.

$ python manage.py runserver

If there are no errors then your application is working flawlessly.

How the application works
---------------------------

* 1. Reads a list of web pages (HTTP URLs) and corresponding page content requirements from a configuration file.
The urls and there contents are saved in an XML file named config.xml. This makes it very easy to modify and make changes. 
    <Configuration>
        <Website>
            <Url>http://www.yahoo.com</Url>
            <Content>my house is good</Content>
        </Website>
    </Configuration>

Configuration.py
------------------
The configuation.py has a Configuration class whose contructor accepts the filename. The filename is made a default argument to makle the class more versatile. This can has a method the returns of tuple of list of url and content. This is a mapping of url ot content. It also have methods for checking the number of websites. It has the checking period. However, since checking period can set the value of the django celery method for running the periodic event. I had to change the design and save the checking period in the settings.py file of the web application.

* 2. Periodically makes an HTTP request to each page.
HTTPClass.py
The HTTPClass class has method that makes the request to the webpage and store the result of request in a convenient structure.  The getresponse method of the class contains a list of lists of all the request objects and attributes. We also save some logging detail with the request object.

* 3. Verifies that the page content received from the server matches the content requirements.
HTTPClass.py
This also have a method that verifies that the content saved in the configuration file matches the content obtained from the web sites. The title of the web page is the variable used for comparing the content as it is less changed and very common in most HTML pages. The class is well documented.

* 4. Measures the time it took for the web server to complete the whole request.
The time is also measured for each request and saved to a suitable structure in the HTTPClass.py file. This done in the getResponses method. We get the time before the request was made and subtract from the time after the request was made.

5. Writes a log file that shows the progress of the periodic checks.
The log file is writing when the periodic event is called in the tasks.py file using django celery instead of the conventional crontab job. The log file can be done with the logging module in python standard library. However, due to time constraint, it is faster writing to a file. The log file has not mechanism for log rotation to prevent file size getting too large. These features will be available in future versions of the project. The cron job is the native way of making scheduled events in Unix. This works very well for most cases. However, this can automate the task by writing events in a scripting language like bash, Tcl etc. However, Django-celery is a real-time asynchronous scheduler that can be used to automate the task. It has many advantages over cron because it understands Python programming language.This project made use of Django-celery to meet all its automation needs.


6. (OPTIONAL) Implement a single-page HTTP server interface in the same process that shows (HTML) each monitored web site and their current (last check) status.
This was done using django web framework. The model.py contains the class that represents the Monitor object. This saved in a mysql database. The view.py contains a method to gets all the Monitor object in the database and display the result in a template. The url.py file matches the view to the url.


The Utils.py file have methods for loading automatically the generated web content on a web browser.

To run a normal python script
python name_of_file.py

When performing unit test
---------------------------
Start a new app
django-admin.py startapp TestMonitor

add the app to the INSTALLED_APP tuple in the settings.py

grant permission to user
GRANT ALL ON test_WebMonitor.* TO 'ken'@'localhost';

run the tests
python manage.py test TestMonitor

The entire source is added inside the Django project folder.
The source tree

WebMonitor
    /logFolder
        log.txt   #log file

    /templates
        base.html   # HTML template for the displayed monitored variables
        index.html  # HTML template for the displayed monitored variables
    /TestMonitor
        __init__.py  
        tests.py

    Configuration.py
    Utils.py
    config.xml        
    settings.py   
    views.py
    HTTPClass.py      
    manage.py     
    urls.py
    __init__.py      
    models.py     
    tasks.py    

The logFolder contains the log file.

The template folder houses all the HTML templates required to run the one paged application.

The TestMonitor folder contain the unittest class. Unit test should be seperate from the application as it may fail.

Configuration.py contains the Configuration class. It has a number of methods of which the most important is the mapping of URL to content.
  
config.xml file contains the weblinks and contents.

Utils.py contains a method for loading the url showing the statistics of the log files.

settings.py contains all the global variables required to run the application. This is where we can set the checking period in form of HOUR, MINUTE and Day_Of_Week variable. The exact description of the values can be found in the setting.py file.

view.py contains the view to be displayed to the user.

HTTPClass.py  contains a method the get all the required attributes of the response from the result in a computer friendly structure. It also wraps some functions from Configuration.py

manage.py This is a script that comes by default in django. It have a number of method for performing administrative tasks.

urls.py This matches the views to the model. It uses regular expression to match the url of the views.

__init__.py needed to show the directory is a python package.

models.py This save the field of the entity to a database.     

tasks.py contains all the periodic task.

The source codes can be found in a compressed file named WebMonitor.tar.gz



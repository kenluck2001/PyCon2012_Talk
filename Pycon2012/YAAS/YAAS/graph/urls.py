from django.conf.urls.defaults import *
from YAAS import settings

urlpatterns = patterns('YAAS.graph.views',
url(r'^(?P<week_no>\d+)/onlUsrBidresultwk.png$', 'weeklyScatterOnlinUsrBid', {'SSL': settings.ENABLE_SSL}, name='Weekly Scatter Diagram of number of online User against number of bids'),

url(r'^(?P<month_no>\d+)/onlUsrBidresultmt.png$', 'monthlyScatterOnlinUsrBid', {'SSL': settings.ENABLE_SSL}, name='Monthly Scatter Diagram of number of online User against number of bids'),

url(r'^(?P<week_no>\d+)/createwkbarchart.png$', 'createWkBarChart',{'SSL': settings.ENABLE_SSL}, name='Bar Graph of number of online user at regular days weekly interval'),

url(r'^(?P<month_no>\d+)/createmthbarchart.png$', 'createMthBarChart',{'SSL': settings.ENABLE_SSL}, name='Bar Graph of number of online user at regular days Monthly interval'),

url(r'^(?P<week_no>\d+)/createwkbarchartregusr.png$', 'createWkBarChartRegUsr',{'SSL': settings.ENABLE_SSL}, name='Bar Graph of number of Registered user at regular days Weekly interval'),

url(r'^(?P<month_no>\d+)/createmthbarchartregusr.png$', 'createMthBarChartRegUsr',{'SSL': settings.ENABLE_SSL}, name='Bar Graph of number of online user at regular days Monthly interval'),

url(r'^disrankitemwithbid.png$', 'displayrankedItemwithBidsPieChart',{'SSL': settings.ENABLE_SSL}, name='Display ranked Item with Bids Pie Chart'),

url(r'^searchstringpiechart.png$', 'searchstringPieChart', {'SSL': settings.ENABLE_SSL}, name='Display searched word with popularity Pie Charts '),

    )

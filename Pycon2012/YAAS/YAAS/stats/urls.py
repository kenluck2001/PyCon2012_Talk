from django.conf.urls.defaults import *
from YAAS import settings

urlpatterns = patterns('YAAS.stats.views',
    url(r'^weeklyregusereport/(?P<week_no>\d+)/$', 'weekRegistdUserReport', {'template_name': 'stats/weeklyRegistdUserReport.html', 'SSL': settings.ENABLE_SSL}, 'Weekly Registered User Report'),

    url(r'^weeklyonlinusereport/(?P<week_no>\d+)/$', 'weekOnlineUserReport', {'template_name': 'stats/weeklyOnlineUserReport.html', 'SSL': settings.ENABLE_SSL}, 'Weekly Online User Report'),


    url(r'^monthlyregusereport/(?P<month_no>\d+)/$', 'monthRegistdUserReport', {'template_name': 'stats/monthlyRegistdUserReport.html', 'SSL': settings.ENABLE_SSL}, 'Monthly Registered User Report'),

    url(r'^monthlyonlinusereport/(?P<month_no>\d+)/$', 'monthOnlineUserReport', {'template_name': 'stats/monthlyOnlineUserReport.html', 'SSL': settings.ENABLE_SSL}, 'Monthly Online User Report'),


    url(r'^yearlyregusereport/$', 'yearRegistdUserReport', {'template_name': 'stats/yearlyRegistdUserReport.html', 'SSL': settings.ENABLE_SSL}, 'Yearly Registered User Report'),

    url(r'^yearlyonlinusereport/$', 'yearOnlineUserReport', {'template_name': 'stats/yearlyOnlineUserReport.html', 'SSL': settings.ENABLE_SSL}, 'Yearly Online User Report'),

    url(r'^allweekreport/$', 'allWeekUserReport', {'template_name': 'stats/allweekReport.html', 'SSL': settings.ENABLE_SSL}, 'All Weeks Report'),

    url(r'^allmonthreport/$', 'allMonthUserReport', {'template_name': 'stats/allmonthReport.html', 'SSL': settings.ENABLE_SSL}, 'All Months Report'),

    url(r'^searchanalysis/$', 'searchstringAnalysis', {'template_name': 'stats/searchanalysis.html', 'SSL': settings.ENABLE_SSL}, 'Search String Analysis'),

    url(r'^bidanalysis/$', 'rankingItemBasedOnBids', {'template_name': 'stats/bidsonitems.html', 'SSL': settings.ENABLE_SSL}, 'Bids On Item Analysis'),

    url(r'^correlation/$', 'onlinUsrBidCor', {'template_name': 'stats/correlation.html', 'SSL': settings.ENABLE_SSL}, 'Correlation of no. of Online Users and Bids made'),

    )

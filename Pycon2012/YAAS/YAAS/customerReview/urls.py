from django.conf.urls.defaults import *
from YAAS import settings


urlpatterns = patterns('YAAS.customerReview.views',
url(r'^customerreview/(?P<bid_id>\d+)/$', 'customerReviewView',{'template_name': 'customerReview/customerViewForm.html'}, 'Customer Review form'),

url(r'^getcustomerreviewitem/(?P<item_id>\d+)/$', 'getCustomerReviewOnItem',{'template_name': 'customerReview/customerReviewResult.html'}, 'Customer Review Result'),

url(r'^custreviewnotification/(?P<review_id>\d+)/$', 'custReviewNotification', {'template_name': 'customerReview/customerReviewNotification.html'},'Customer Review Notification'),

    )

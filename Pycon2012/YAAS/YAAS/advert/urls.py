from django.conf.urls.defaults import *
from YAAS import settings

urlpatterns = patterns('YAAS.advert.views',
    (r'^advertform/$','advert_create',{'template_name': 'adverts/advertForm.html', 'SSL': settings.ENABLE_SSL }, 'Advertisement form'),

    (r'^showalladverts/$','showAllAdverts',{'template_name': 'adverts/showadverts.html'}, 'Show All Advert'),

    (r'^advertdetails/(?P<advert_id>\d+)/$','getAdvertDetails',{'template_name': 'adverts/advertdetails.html', 'SSL': settings.ENABLE_SSL}, 'Advert Details'),

)

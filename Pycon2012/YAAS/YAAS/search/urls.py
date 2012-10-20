from django.conf.urls.defaults import *

urlpatterns = patterns('YAAS.search.views',
    (r'^results/$','results',{'template_name': 'search/results.html'}, 'search_results'),
)

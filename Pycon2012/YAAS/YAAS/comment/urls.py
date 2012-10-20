from django.conf.urls.defaults import *

urlpatterns = patterns('YAAS.comment.views',
    url(r'^(?P<item_id>\d+)/$', 'base', {'template_name': 'comment/base.html'}, 'send message'),
    url(r'^(?P<item_id>\d+)/messages/$', 'messages', {'template_name': 'comment/messages.html'}, 'receive message' ),
    )



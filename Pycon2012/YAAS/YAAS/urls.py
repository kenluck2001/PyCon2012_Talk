#from django.conf.urls.defaults import patterns, include, url
import os
#from YAAS.views. import *
from YAAS import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

skip_last_activity_date = [
    #Your expressions go here
]



#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YAAS.views.home', name='home'),
    # url(r'^YAAS/', include('YAAS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#	(r'^catalog/$', 'YAAS.views.catalog'),

#)

urlpatterns = patterns('',
	# other commented code here
	(r'^admin/', include(admin.site.urls)),

	#(r'^accounts/', include('django.contrib.auth.urls')),


	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
		{ 'document_root' : os.path.join(settings.CURRENT_PATH, 'static') }
	),
	(r'^account/login/$', 'YAAS.views.login',{'template_name': 'account/login.html', 'SSL': settings.ENABLE_SSL}, 'login'),

	(r'^account/register/$', 'YAAS.views.register',{'template_name': 'account/register.html', 'SSL': settings.ENABLE_SSL}, 'register'),

	(r'^account/confirm/(?P<activation_key>\w+)/$', 'YAAS.views.confirm',{'template_name': 'account/confirm.html', 'SSL': settings.ENABLE_SSL }, 'confirm'),

	(r'^account/edit/$', 'YAAS.views.edit_account',{'template_name': 'account/update.html', 'SSL': settings.ENABLE_SSL}, 'edit_account'),

	(r'^account/passwordchange/$', 'YAAS.views.password_change',{'template_name': 'account/password_change.html', 'SSL': settings.ENABLE_SSL}, 'password_change'),

	(r'^account/logout/$', 'YAAS.views.logoutview', {'template_name': 'account/logout.html', 'SSL': settings.ENABLE_SSL}, 'logout'),

	(r'^auction/makebid/(?P<item_id>\d+)/$', 'YAAS.views.makebid',{'template_name': 'auction/makebid.html'}, 'makebid'),

	(r'^auction/createauction/$', 'YAAS.views.auction_create',{'template_name': 'auction/createauction.html'}, 'auction_create'),

	(r'^auction/updateauction/(?P<item_id>\d+)/$', 'YAAS.views.auction_update',{'template_name': 'auction/updateauction.html'}, 'auction_update'),

	(r'^auction/showmycreatedauction/$', 'YAAS.views.showAllCreatedAuction',{'template_name': 'auction/showauction.html'}, 'showAllCreatedAuction'),

	(r'^auction/showmybid/$', 'YAAS.views.showAllMadeBid',{'template_name': 'auction/showbid.html'}, 'showAllMadeBid'),

	(r'^auction/showcurrentbid/(?P<bid_id>\d+)/$', 'YAAS.views.showCurrentBid',{'template_name': 'auction/showNewbid.html'}, 'showCurrentBid'),

	(r'^auction/showcurrentitem/(?P<item_id>\d+)/$', 'YAAS.views.showCurrentItem',{'template_name': 'auction/showNewCreatedItem.html'}, 'showCurrentItem'),

	(r'^auction/showcurrentupdatedbid/(?P<bid_id>\d+)/$', 'YAAS.views.showCurrentUpdatedBid',{'template_name': 'auction/showupdatedbid.html'}, 'showCurrentUpdatedBid'),

	(r'^auction/showcurrentupdateditem/(?P<item_id>\d+)/$', 'YAAS.views.showCurrentUpdatedItem',{'template_name': 'auction/showupdatedItem.html'}, 'showCurrentUpdatedItem'),

	(r'^account/my_account/$', 'YAAS.views.my_account',{'template_name': 'account/my_account.html'}, 'my_account'),

	(r'^auction/getbidsonitem/(?P<itemid>\d+)/$', 'YAAS.views.getBidsOnItem',{'template_name': 'auction/bidsfromitem.html'}, 'getBidsOnItem'),

	(r'^auction/getitemdetails/(?P<item_id>\d+)/$', 'YAAS.views.getItemDetails',{'template_name': 'auction/itemdetails.html'}, 'getItemDetails'),

	(r'^auction/getpicture/(?P<item_id>\d+)/$', 'YAAS.views.getPicture',{'template_name': 'auction/itempictures.html'}, 'getItemPicture'),

	(r'^index/$', 'YAAS.views.indexView',{'template_name': 'index.html'}, 'index'),

	#search functionality
	(r'^search/', include('YAAS.search.urls')),

	#advertisement functionality
	(r'^advert/', include('YAAS.advert.urls')),

	#chat functionality
	(r'^comment/', include('YAAS.comment.urls')),

	#capcha to prevent spam
    (r'^captcha/', include('YAAS.captcha.urls')),

	#generate statistical reports
    (r'^stats/', include('YAAS.stats.urls')),

	#generate statistical graphs
    (r'^graph/', include('YAAS.graph.urls')),

	#generate customer review
    (r'^review/', include('YAAS.customerReview.urls')),
)




#http://bitkickers.blogspot.com/2010/07/djangocelery-quickstart-or-how-i.html

from YAAS.models import Item, Bid 
from YAAS.stats.models import RegisteredUser, OnlineUser, StatBid
from YAAS.stats import stat
from django.template import RequestContext, Context,  loader
from django.core.mail import send_mail, EmailMessage
from celery.task.schedules import crontab  
from celery.decorators import periodic_task 
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


#make the items invisible
def makeAllItemsInvisible():
	itemQuerySet = Item.objects.all()
	itemQuerySet.update(status=False)

#make the bids invisible
def makeAllBidsInvisible():
	bidQuerySet = Bid.objects.all()
	bidQuerySet.update(availability=False)

#make the items visible
def makeAllItemsVisible():
	itemQuerySet = Item.objects.all()
	itemQuerySet.update(status=True)

#make the bids visible
def makeAllBidsVisible():
	bidQuerySet = Bid.objects.all()
	bidQuerySet.update(availability=True)

#resolve auction
@periodic_task(run_every=crontab(hour=1, minute=15, day_of_week="*"))  
def resolveAuction():
	#make item and bid invisible
	makeAllItemsInvisible()
	makeAllBidsInvisible()

	#change bid status to resolved after time lapse
	threedays = datetime.today() -  timedelta(days=3)

	myItem = Item.objects.filter(end_date__lte=threedays)
	for item in myItem:
	    myBid_id = Bid.objects.filter(item=item).order_by('-bid_price')
	    for b_id in myBid_id:
		    bid_obj = get_object_or_404( Bid, pk=int(b_id.id) )
		    bid_obj.is_winner=True
		    bid_obj.save()
            break

	realBid = Bid.objects.exclude(is_emailed=True).filter(item__end_date__lte=threedays)
	for bid in realBid:  
		bid_obj = get_object_or_404( Bid, pk=int( bid.id)  )
		if bid_obj.is_winner:
			#send email to winner
			t = loader.get_template('registration/winnerBid.txt')
			c = Context({
				'firstname': 		bid_obj.user.first_name,
				'lastname': 		bid_obj.user.last_name,
				'site_name': 		'YAAS Auction Site',
				'admin': 			'Kenneth Odoh',
				'bid_id':			bid_obj.id,
			})

			email_subject = 'Your have won the auction YAAS account'
			send_mail(email_subject, t.render(c), 'account@example.com', [bid_obj.user.email], fail_silently=False) 
			bid_obj.is_emailed=True 

        else:

            t = loader.get_template('registration/otherBidder.txt')
            c = Context({
				'firstname': 		bid_obj.user.first_name,
				'lastname': 		bid_obj.user.last_name,
				'site_name': 		'YAAS Auction Site',
				'admin': 			'Kenneth Odoh',
			})

            recipientlist = list(Bid.objects.exclude(is_emailed=True).values_list('user__email', flat=True))
            bid_obj.is_emailed=True
            email_subject = 'Your auction has been resolved'
            core_msg = EmailMessage(subject=email_subject, body=t.render(c), from_email='account@example.com', to=recipientlist)
            core_msg.send(fail_silently=False)
		

	#auction has been resolved so maintenance is over
	makeAllItemsVisible()
	makeAllBidsVisible()


@periodic_task(run_every=crontab(hour=1, minute=25, day_of_week="*"))
def makeExpiredItemsBidInvisible():
	threedays = datetime.today() - datetime.timedelta(days=3)
	myItem = Item.objects.filter(end_date__lte=threedays )
	myItem.update(status=False)
	myBid = Bid.objects.filter(item__in=myItem)
	myBid.update(availability=False)


@periodic_task(run_every=crontab(hour=1, minute=30, day_of_week=0))
def deleteOldItemsandBids():
	hunderedandtwentydays = datetime.today() - datetime.timedelta(days=120)
	myItem = Item.objects.filter(end_date__lte=hunderedandtwentydays ).delete()
	myBid = Bid.objects.filter(end_date__lte=hunderedandtwentydays ).delete()

#populate the registereduser and onlineuser model at regular intervals

@periodic_task(run_every=crontab(hour=1, minute=45, day_of_week="*"))
def fillRegisterUserModel():
	regnum = stat.getNumofRegisteredUser()
	n_day = stat.getDay()
	n_month = stat.getMonth()
	n_year = stat.getYear()
	n_week = stat.getWeek(n_day, n_month, n_year)
	regUsrObj = RegisteredUser(no_of_reg_user=regnum, day=n_day,	month=n_month, 	year=n_year, week=n_week)

	regUsrObj.save()

def fillOnlineUserModel():
	onlnum = stat.getNumofOnlineUser()
	n_day = stat.getDay()
	n_month = stat.getMonth()
	n_year = stat.getYear()
	n_week = stat.getWeek(n_day, n_month, n_year)
	onlinUsrObj = OnlineUser(no_of_online_user=onlnum, day=n_day,	month=n_month, 	year=n_year, week=n_week)

	onlinUsrObj.save()


def fillStatBidModel():
	numbid = stat.getNumofBid()
	n_day = stat.getDay()
	n_month = stat.getMonth()
	n_year = stat.getYear()
	n_week = stat.getWeek(n_day, n_month, n_year)
	bidObj = StatBid(no_of_bids=numbid, day=n_day,	month=n_month, 	year=n_year, week=n_week)

	bidObj.save()

@periodic_task(run_every=crontab(hour="*/7", minute=50, day_of_week="*"))
def realwork():
    fillOnlineUserModel()
    fillStatBidModel()
    

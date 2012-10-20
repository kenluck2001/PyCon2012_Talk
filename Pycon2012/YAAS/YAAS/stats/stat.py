from datetime import datetime, timedelta, date
import operator
from YAAS.models import CustomUser
from YAAS.lastActivityDate.models import UserActivity
from YAAS.models import Item, Bid

	
def getNumofRegisteredUser():
    usercount = CustomUser.objects.filter(is_active=True).count()
    return usercount

def getDay():
    return datetime.now().day

def getMonth():
    return datetime.now().month

def getYear():
    return datetime.now().year

def getWeek(n_day, n_month, n_year):
	return date(n_year, n_month, n_day).isocalendar()[1]

def getNumofOnlineUser():
    fifteen_minutes = datetime.now() - timedelta(minutes=15)
    sql_datetime = datetime.strftime(fifteen_minutes, '%Y-%m-%d %H:%M:%S')
    users_count = UserActivity.objects.filter(last_activity_date__gte=sql_datetime, user__is_active__exact=1).count()
    return users_count 

#This is used to calculate the ranking of amount of bids made on items
def createItemIDBidCountDict():
    items = Item.active.all()
    result = {}
    bdSum=0
    bidcount=0
    for item in items:
        bids = Bid.active.filter(item = item)
        bidcount = bids.count()
        bdSum+=bidcount
        result[item.id] = bidcount  
    return result, bdSum

	
#sort dictionary by value
def sortedItemDictionary(x):
    sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]
    return sorted_x

#get number of bid
def getNumofBid():
    bidcount = Bid.active.count()
    return bidcount

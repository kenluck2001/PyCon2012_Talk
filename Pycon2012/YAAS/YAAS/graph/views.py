from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from YAAS.stats.models import RegisteredUser, OnlineUser, StatBid
from YAAS.search.models import SearchTerm
from YAAS.models import Item
from YAAS.stats import stat
from YAAS.stats import thinkstats, correlation
from django.shortcuts import get_object_or_404
from collections import Counter
from django.contrib.admin.views.decorators import staff_member_required


#scatter diagram of number of bids made against number of online users
# weekly report
@staff_member_required
def weeklyScatterOnlinUsrBid(request, week_no):
    page_title='Weekly Scatter Diagram based on Online user verses Bid'
    weekno=week_no
    fig=Figure()
    ax=fig.add_subplot(111)
    year=stat.getYear()
    onlUserObj = OnlineUser.objects.filter(week=weekno).filter(year=year)
    bidObj = StatBid.objects.filter(week=weekno).filter(year=year)
    onlUserlist = list(onlUserObj.values_list('no_of_online_user', flat=True))
    bidlist = list(bidObj.values_list('no_of_bids', flat=True))
    title='Scatter Diagram of number of online User against number of bids (week {0}) {1}'.format(weekno,year)
    ax.set_xlabel('Number of online Users')
    ax.set_ylabel('Number of Bids')
    fig.suptitle(title, fontsize=14)
    try:
        ax.scatter(onlUserlist, bidlist)
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

# monthly report
@staff_member_required
def monthlyScatterOnlinUsrBid(request, month_no):
    page_title='Monthly Scatter Diagram based on Online user verses Bid'
    monthno=month_no
    monthsDict = {1 : "January", 2 : "February", 3 :	"March", 4 : "April", 5 : "May",6 : "June",7 : "July",8 :	"August",9 : "September",10 : "October",11 : "November",12 :	"December"}
    realMonth = monthsDict[int(monthno)]
    fig=Figure()
    ax=fig.add_subplot(111)
    year=stat.getYear()
    onlUserObj = OnlineUser.objects.filter(month=monthno).filter(year=year)
    bidObj = StatBid.objects.filter(month=monthno).filter(year=year)
    onlUserlist = list(onlUserObj.values_list('no_of_online_user', flat=True))
    bidlist = list(bidObj.values_list('no_of_bids', flat=True))
    title='Scatter Diagram of number of online User against number of bids ({0} {1})'.format(realMonth,year)
    ax.set_xlabel('Number of online Users')
    ax.set_ylabel('Number of Bids')
    fig.suptitle(title, fontsize=14)
    try:
        ax.scatter(onlUserlist, bidlist)
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

#create a bar chart of total online user at regular interval
#weekly
@staff_member_required
def createWkBarChart(request, week_no):
    page_title='Weekly Bar Chart' 
    weekno=week_no
    fig=Figure()
    ax=fig.add_subplot(111)
    year=stat.getYear()
    onlUserObj = OnlineUser.objects.filter(week=weekno).filter(year=year)
    noofuserlist = list(onlUserObj.values_list('no_of_online_user', flat=True))
    daylist = list(onlUserObj.values_list('day', flat=True))
    daylist = [day-0.4  for day in daylist]

    title='Bar Graph of number of online user at regular days interval (week ({0}) {1})'.format(weekno,year)
    ax.set_xlabel('Days')
    ax.set_ylabel('Number of Online User')
    fig.suptitle(title, fontsize=14) 
    try:
        ax.bar(daylist, noofuserlist)
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

#monthly
@staff_member_required
def createMthBarChart(request, month_no):
    page_title='Monthly Bar Chart'
    monthno=month_no
    fig=Figure()
    ax=fig.add_subplot(111)
    year=stat.getYear()
    onlUserObj = OnlineUser.objects.filter(month=monthno).filter(year=year)
    noofuserlist = list(onlUserObj.values_list('no_of_online_user', flat=True))
    daylist = list(onlUserObj.values_list('day', flat=True))
    daylist = [day-0.4  for day in daylist]
    monthsDict = {1 : "January", 2 : "February", 3 :	"March", 4 : "April", 5 : "May",6 : "June",7 : "July",8 :	"August",9 : "September",10 : "October",11 : "November",12 :	"December"}
    realMonth = monthsDict[int(monthno)]
    title='Bar Graph of number of online user at regular days interval ({0} {1})'.format(realMonth,year)
    ax.set_xlabel('Days')
    ax.set_ylabel('Number of Online User')
    fig.suptitle(title, fontsize=14)
    try:
        ax.bar(daylist, noofuserlist);
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


#create a bar chart of total Registered user at regular interval
#weekly
@staff_member_required
def createWkBarChartRegUsr(request, week_no):
    page_title='Weekly Bar Chart on Registered User'
    weekno=week_no
    fig=Figure()
    ax=fig.add_subplot(111)
    year=stat.getYear()
    RegdUserObj = RegisteredUser.objects.filter(week=weekno).filter(year=year)
    noofuserlist = list(RegdUserObj.values_list('no_of_reg_user', flat=True))
    daylist = list(RegdUserObj.values_list('day', flat=True))
    daylist = [day-0.4  for day in daylist]
    title='Bar Graph of number of Registered User at regular days interval (week {0} {1})'.format(weekno,year)
    ax.set_xlabel('Days')
    ax.set_ylabel('Number of Registered User')
    fig.suptitle(title, fontsize=14)
    try:
        ax.bar(daylist, noofuserlist);
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

#monthly
@staff_member_required
def createMthBarChartRegUsr(request, month_no):
    page_title='Monthly Bar Chart on Registered User'
    monthno=month_no
    fig=Figure()
    ax=fig.add_subplot(111)
    year=stat.getYear()
    onlUserObj = OnlineUser.objects.filter(month=monthno).filter(year=year)
    noofuserlist = list(onlUserObj.values_list('no_of_online_user', flat=True))
    daylist = list(onlUserObj.values_list('day', flat=True))
    daylist = [day-0.4  for day in daylist]
    monthsDict = {1 : "January", 2 : "February", 3 :	"March", 4 : "April", 5 : "May",6 : "June",7 : "July",8 :	"August",9 : "September",10 : "October",11 : "November",12 :	"December"}
    realMonth = monthsDict[int(monthno)]
    title='Bar Graph of number of Registered user at regular days interval ({0} {1})'.format(realMonth,year)
    ax.set_xlabel('Days')
    ax.set_ylabel('Number of Registered User')
    fig.suptitle(title, fontsize=14)
    try:
        ax.bar(daylist, noofuserlist);
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

@staff_member_required
def displayrankedItemwithBidsPieChart(request):
    page_title='Pie Chart on Ranked Item'
    year=stat.getYear()
    itemBidDict, bidtotalSum = stat.createItemIDBidCountDict()
    top_ten_dict = stat.sortedItemDictionary(itemBidDict)
    itemobjDict = {}	
    for key,value in top_ten_dict:
        itemObj = get_object_or_404(Item, pk=key)
        itemobjDict[itemObj.name] = value

    fig=Figure()
    ax=fig.add_subplot(111)

    title='Top Ten ranked items with the highest bids ({0})'.format(year)
    fig.suptitle(title, fontsize=14)
    try:
        x = itemobjDict.values()
        labels = itemobjDict.keys()
        ax.pie(x, labels=labels);
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

#analysis of search strings
@staff_member_required
def searchstringPieChart(request):
    page_title='Search String Pie Chart'
    year=stat.getYear()
    searchList = list(SearchTerm.objects.values_list('q', flat=True))
    search_string = ' '.join(searchList)
    result = Counter(search_string.split()).most_common(10)
    searchDict = {}
    for key,val in result:
        searchDict[key] = val

    fig=Figure()
    ax=fig.add_subplot(111)

    title='Top Ten search string submitted by user ({0})'.format(year)
    fig.suptitle(title, fontsize=14)
    try:
        x = searchDict.values()
        labels = searchDict.keys()
        ax.pie(x, labels=labels);
    except 	ValueError:
        pass
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

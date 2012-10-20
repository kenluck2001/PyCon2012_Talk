from datetime import datetime
from YAAS.models import CustomUser
from YAAS.stats.models import RegisteredUser, OnlineUser, StatBid
from YAAS.stats import stat
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from YAAS.search.models import SearchTerm
from collections import Counter
from YAAS.models import Item
from YAAS.stats import thinkstats, correlation
from django.contrib.admin.views.decorators import staff_member_required

# weekly report
@staff_member_required
def weekRegistdUserReport(request, week_no, template_name="stats/weeklyRegistdUserReport.html"):
    page_title='Weekly Registered User Report'
    weekno=week_no
    year=stat.getYear()
    RegUserObj = RegisteredUser.objects.filter(week=weekno).filter(year=year)
    regobjlist=list(RegUserObj.values_list('no_of_reg_user', flat=True))
    mean ="N/A"
    variance="N/A"
    try:
        mean = "{0:.2f}".format(thinkstats.Mean(regobjlist))
        variance= "{0:.2f}".format(thinkstats.Var(regobjlist))
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@staff_member_required
def weekOnlineUserReport(request, week_no, template_name="stats/weeklyOnlineUserReport.html"):
    page_title='Weekly Online User Report'
    weekno=week_no
    year=stat.getYear()
    OnlineObj = OnlineUser.objects.filter(week=weekno).filter(year=year)
    onlobjlist=list(OnlineObj.values_list('no_of_online_user', flat=True))
    mean ="N/A"
    variance="N/A"
    try:
        mean = "{0:.2f}".format(thinkstats.Mean(onlobjlist))
        variance= "{0:.2f}".format(thinkstats.Var(onlobjlist))
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

#monthly report
@staff_member_required
def monthRegistdUserReport(request, month_no, template_name="stats/monthlyRegistdUserReport.html"):
    page_title='Monthly Registered User Report'
    monthno=month_no
    year=stat.getYear()
    monthsDict = {1 : "January", 2 : "February", 3 :	"March", 4 : "April", 5 : "May",6 : "June",7 : "July",8 :	"August",9 : "September",10 : "October",11 : "November",12 :	"December"}
    realMonth = monthsDict[int(monthno)]
    RegUserObj = RegisteredUser.objects.filter(month=monthno).filter(year=year)
    regobjlist=list(RegUserObj.values_list('no_of_reg_user', flat=True))
    mean ="N/A"
    variance="N/A"
    try:
        mean = "{0:.2f}".format(thinkstats.Mean(regobjlist))
        variance= "{0:.2f}".format(thinkstats.Var(regobjlist))
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@staff_member_required
def monthOnlineUserReport(request, month_no, template_name="stats/monthlyOnlineUserReport.html"):
    page_title='Monthly Online User Report'
    monthno=month_no
    year=stat.getYear()
    monthsDict = {1 : "January", 2 : "February", 3 :	"March", 4 : "April", 5 : "May",6 : "June",7 : "July",8 :	"August",9 : "September",10 : "October",11 : "November",12 :	"December"}
    realMonth = monthsDict[int(monthno)]
    OnlineObj = OnlineUser.objects.filter(month=monthno).filter(year=year)
    onlobjlist=list(OnlineObj.values_list('no_of_online_user', flat=True))
    mean ="N/A"
    variance="N/A"
    try:
        mean = "{0:.2f}".format(thinkstats.Mean(onlobjlist))
        variance= "{0:.2f}".format(thinkstats.Var(onlobjlist))
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

#yearly report
@staff_member_required
def yearRegistdUserReport(request, template_name="stats/yearlyRegistdUserReport.html"):
    page_title='Yearly Registered User Report'
    year=stat.getYear()
    RegUserObj = RegisteredUser.objects.filter(year=year)
    regobjlist=list(RegUserObj.values_list('no_of_reg_user', flat=True))
    mean ="N/A"
    variance="N/A"
    try:
        mean = "{0:.2f}".format(thinkstats.Mean(regobjlist))
        variance= "{0:.2f}".format(thinkstats.Var(regobjlist))
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@staff_member_required
def yearOnlineUserReport(request, template_name="stats/yearlyOnlineUserReport.html"):
    page_title='Yearly Online User Report'
    year=stat.getYear()
    OnlineObj = OnlineUser.objects.filter(year=year)
    onlobjlist=list(OnlineObj.values_list('no_of_online_user', flat=True))
    mean ="N/A"
    variance="N/A"
    try:
        mean = "{0:.2f}".format(thinkstats.Mean(onlobjlist))
        variance= "{0:.2f}".format(thinkstats.Var(onlobjlist))
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

#display all week report
@staff_member_required
def allWeekUserReport(request, template_name="stats/allweekReport.html"):
    page_title="All Week's User Report"
    weeklist = [x for x in range(1,53)]
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

#display all month report
@staff_member_required
def allMonthUserReport(request, template_name="stats/allmonthReport.html"):
    page_title="All Month's User Report"
    monthsDict = {1 : "January", 2 : "February", 3 :	"March", 4 : "April", 5 : "May",6 : "June",7 : "July",8 :	"August",9 : "September",10 : "October",11 : "November",12 :	"December"}
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

#analysis of search strings
@staff_member_required
def searchstringAnalysis(request, template_name="stats/searchanalysis.html"):
    page_title="Search Analysis Report"
    searchList = list(SearchTerm.objects.values_list('q', flat=True))
    search_string = ' '.join(searchList)
    total_count = len(searchList)
    result = Counter(search_string.split()).most_common(10)
    sumtotal=0
    valuelist=[]
    mean ="N/A"
    variance="N/A"
    for key, value in result:
        sumtotal+=value
        valuelist.append(value)
    percentTotal=0.00
    try:
        percentTotal= (sumtotal / total_count) * 100
        mean = "{0:.2f}".format(thinkstats.Mean(valuelist))
        variance= "{0:.2f}".format(thinkstats.Var(valuelist))
    except 	ZeroDivisionError:
        pass
    percentTotalString="{0:.2f}".format(percentTotal)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@staff_member_required
def rankingItemBasedOnBids(request, template_name="stats/bidsonitems.html"):
    page_title="Ranking Item based on Bids Report"
    itemBidDict, bidtotalSum = stat.createItemIDBidCountDict()
    top_ten_dict = stat.sortedItemDictionary(itemBidDict)
    bidSum=0
    valuelist=[]
    itemobjDict = {}	
    mean ="N/A"
    variance="N/A"
    for key,value in top_ten_dict:
        itemObj = get_object_or_404(Item, pk=key)
        itemobjDict[itemObj] = value
        bidSum+=value
        valuelist.append(value)
    percentTotal= 0.00
    try:
        percentTotal= (bidSum / bidtotalSum) * 100
        mean = "{0:.2f}".format(thinkstats.Mean(valuelist))
        variance= "{0:.2f}".format(thinkstats.Var(valuelist))
    except 	ZeroDivisionError:
        pass
    percentTotalString="{0:.2f}".format(percentTotal)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

#correlation between number of online user and bids that have been made
@staff_member_required
def onlinUsrBidCor(request, template_name="stats/correlation.html"):
    OnlineObj = OnlineUser.objects.all()
    onlobjlist = list(OnlineObj.values_list('no_of_online_user', flat=True)) 
    statbidObj = StatBid.objects.all()
    statbidlist = list(statbidObj.values_list('no_of_bids', flat=True))
    spearCor = "N/A"
    listlenght = 0
    if len(onlobjlist) <= len(statbidlist) :
        listlenght = len(onlobjlist)
    else:
        listlenght = len(statbidlist)
    #modify the length of the list to prevent issues

    try:
        modOnlinList = onlobjlist[0 : listlenght]
        modbidlist = statbidlist[0 : listlenght]  

        spearCor = "{0:.3f}".format( correlation.SpearmanCorr(modOnlinList, modbidlist) )
    except 	ZeroDivisionError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
     


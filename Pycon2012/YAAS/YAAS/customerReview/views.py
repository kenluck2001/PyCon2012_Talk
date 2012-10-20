from django.template import RequestContext, Context,  loader, Template
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from YAAS.models import CustomUser, Bid, Item
from YAAS.customerReview.models import ProductReview
from YAAS.customerReview.forms import ProductReviewForm

def customerReviewView(request, bid_id, template_name="customerReview/customerViewForm.html"):
    '''
        This creates the customer review form
    '''
    page_title='Customer Review form'
    bidno = int(bid_id)
    if request.method == 'POST' and request.user.is_authenticated():
        postdata = request.POST.copy()
        form = ProductReviewForm(postdata)
        bdObj = get_object_or_404(Bid, pk=bidno)
        usrObj = get_object_or_404(CustomUser, pk=request.user.id)
        if form.is_valid() and usrObj == bdObj.user and bdObj.is_winner:
            human = True
            rating = postdata.get('rating','')
            comment = postdata.get('comment','')
            prodRevObj = ProductReview(rating=rating, comment=comment)
            prodRevObj.save()
            bdObj.review = prodRevObj
            bdObj.save()
            return HttpResponseRedirect(reverse('YAAS.customerReview.views.custReviewNotification', args=(prodRevObj.id,)))
    else:
        form = ProductReviewForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def getCustomerReviewOnItem(request, item_id, template_name="customerReview/customerReviewResult.html"):	
    '''
        This displays the customer view on the item. This hooks up the owner of the item and rates the owner of the item that the user is about to bid. He can use the information to indentify the credibility of the seller.
    '''
    page_title='Customer Review Result'
    itemObj = get_object_or_404(Item, pk=int(item_id))
    itemQuerySet = Item.objects.filter(owner=itemObj.owner)
    bidObject = Bid.objects.filter(item__in=itemQuerySet).filter(is_winner=True)[0:10]
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))




def custReviewNotification(request, review_id, template_name="customerReview/customerReviewNotification.html"):
    '''
        This displays the current created customer review
    '''
    page_title='Customer Review Notification'
    prodReviewObj = get_object_or_404(ProductReview, pk=int(review_id))
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

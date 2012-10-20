from django.template import RequestContext, Context,  loader, Template
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from YAAS import extra
from YAAS.forms import LoginForm, RegistrationForm, EditForm, AuctionForm, BidForm, PasswordForm
from YAAS.models import CustomUser, Item, Bid 
from django.core.mail import send_mail, EmailMessage
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from datetime import datetime, timedelta  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.hashcompat import sha_constructor
import datetime, random
import decimal
from YAAS.advert.models import Advertisement


def login(request, template_name="account/login.html"):
    '''
		This is form is used to make a user login.
    '''
    if request.method == 'POST':
        postdata = request.POST.copy()
        page_title='Login form'
        form = LoginForm(request, postdata)
        if form.is_valid():
            un = postdata.get('username','')
            pw = postdata.get('password','')
            hashpw = extra.hashPassword(pw)
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=hashpw)
            if new_user and new_user.is_active:
                login(request, new_user)
                request.session['session_id'] = extra.generate_session_id()
                return HttpResponseRedirect(reverse('my_account'))
            else:
                return render_to_response('errors/login.html',
                          context_instance=RequestContext(request))
    else:
        form = LoginForm(request=request, label_suffix=':')

        # set the test cookie on our first GET request
        request.session.set_test_cookie()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def register(request, template_name="account/register.html"):
    '''
	    This allows the anonymous user to become a registered user.
		This is the form used to register a new user and sends email with the action link with a time out.
    '''
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return HttpResponseRedirect(reverse('YAAS.views.my_account'))
    if request.method == 'POST':
        postdata = request.POST.copy()
        page_title='Registration  form'
        form = RegistrationForm(postdata)
        if form.is_valid():          
            # Build the activation key for their  account  
            human = True        
            un = postdata.get('user_name','')
            pw = postdata.get('pass_word','')  
            em = postdata.get('email','') 
            fn = postdata.get('first_name','')  
            ln = postdata.get('last_name','')    
            pn = postdata.get('phone_number','') 
            sx = postdata.get('sex','')  


            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            activation_key = sha_constructor(salt+un).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
  
            # Create and save their profile  
            hashpw = extra.hashPassword(pw)
            new_profile = CustomUser.objects.create_user(username=un, email=em,  password=hashpw)

            new_profile.is_active = False
            new_profile.first_name = fn
            new_profile.last_name = ln
            new_profile.activation_key = activation_key
            new_profile.keyexpiry_date = key_expires
            new_profile.phone_number = pn
            new_profile.sex = sx   
                                                                                                    
            new_profile.save()

            t = loader.get_template('registration/email.txt')
            c = Context({
				'firstname': 		new_profile.first_name,
				'lastname': 		new_profile.last_name,
				'site_name': 		'YAAS Auction Site',
				'username': 		new_profile.username,
				'activationkey': 	new_profile.activation_key,
				'admin': 			'Kenneth Odoh',
			})

            email_subject = 'Your new YAAS account'
            send_mail(email_subject, t.render(c), 'account@example.com', [new_profile.email], fail_silently=False)   
            return HttpResponseRedirect(reverse('my_account'))
    else:
        #errors 
        form = RegistrationForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

'''
	This allows the newly registered user to activate their action
'''
def confirm(request, activation_key,template_name="account/confirm.html"):
    '''
        This is used to generate the activation links. This has a expiry date.
    '''
    page_title='User Confirmation form'
    if request.user.is_authenticated():
        has_account=True
        return HttpResponseRedirect(reverse('my_account'))
    user_profile = get_object_or_404(CustomUser, activation_key=activation_key)
    if user_profile.keyexpiry_date > datetime.datetime.today():
        expired=False
        user_profile.is_active = True
        user_profile.save()
        return HttpResponseRedirect(reverse('login'))
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



def edit_account(request, template_name="account/update.html"):
    '''
	    This allows the registered user to alter user registered information. This is used to changes to user's data.
    '''
    if request.method == 'POST' and request.user.is_authenticated():
        page_title='Edit User Information form'
        postdata = request.POST.copy()
        form = EditForm(postdata)
        if form.is_valid():  
            human = True
            user_profile = get_object_or_404(CustomUser, pk=request.user.id)

            email = postdata.get('email','') 
            first_name = postdata.get('first_name','')  
            last_name = postdata.get('last_name','')    
            phone_number = postdata.get('phone_number','') 
            sex = postdata.get('sex','') 

            my_list = []

            if first_name <> '':
                user_profile.first_name = first_name
                my_list.append("first name")

            if last_name <> '':
                user_profile.last_name = last_name
                my_list.append("last name")

            if email <> '':
                user_profile.email = email
                my_list.append("email")

            if phone_number <> '':
                user_profile.phone_number = phone_number
                my_list.append("phone name")

            if sex <> '':
                user_profile.sex = sex
                my_list.append("sex")

            user_profile.save()
            t = loader.get_template('registration/update.txt')
            c = Context({
				'firstname': 		new_profile.first_name,
				'lastname': 		new_profile.last_name,
				'site_name': 		'YAAS Auction Site',
				'admin': 			'Kenneth Odoh',
				'my_list':			my_list,

			})

            email_subject = 'Your YAAS account has been updated'
            send_mail(email_subject, t.render(c), 'account@example.com', [new_profile.email], fail_silently=False) 
            return HttpResponseRedirect(reverse('my_account'))
    else:
        #errors 
        form = EditForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def password_change(request, template_name="account/password_change.html"):
    '''
	    This allows the registered user to change their password
    '''
    if request.method == 'POST' and request.user.is_authenticated():
        page_title='Password Change form'
        postdata = request.POST.copy()
        form = PasswordForm(CustomUser,postdata)
        if form.is_valid():
            human = True
            pw = postdata.get('new_password','')
            user_profile = get_object_or_404(CustomUser, pk=request.user.id)
            hashpw = extra.hashPassword(pw)
            user_profile.set_password(hashpw)
            user_profile.save()
			#force user log out
            return HttpResponseRedirect(reverse('login'))
    else:
        form = PasswordForm(CustomUser)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


#	This allows the registered user to log out of the site

def logoutview(request, template_name="account/logout.html"):
    page_title='Logout form'
    try:
        del request.session['session_id']
    except KeyError:
        pass
    logout(request)
    return render_to_response(template_name,locals(), context_instance=RequestContext(request))



@login_required(login_url='/account/login/')
def makebid(request, item_id, template_name="auction/makebid.html"):
    '''
	    This allows the registered user to make bids on the site. The bids are arranged in a list that deletes duplicate. Every new bids must be higher than all previous bids. However, since duplicates are eliminated every bid is unique. We cannot have a bid with the same amount twice. The bids are sorted according to bid amount and bid date. Therefore the first element in the list is always the highest bid. We can obtain the value use the index 0. Email is sent whenever a bid is made. You cannot bid on the item that you created.
    '''
    itemid = item_id
    item = get_object_or_404(Item, pk=itemid)
    page_title='Make Bid form'
 
    if request.method == 'POST' and request.user.is_authenticated():
        postdata = request.POST.copy()
        form = BidForm(postdata)
        user_profile = get_object_or_404(CustomUser, pk=request.user.id)
        bidQuerySet = Bid.active.filter(item=item)
        highest_bid_list = list(bidQuerySet.order_by('-bid_price').values_list('bid_price', flat=True))
               
        if form.is_valid() and user_profile != item.owner:
            human = True
            amount = postdata.get('amount') 
            decAmount= decimal.Decimal(str(amount))
            dechighBid= decimal.Decimal(str(item.highestbid))
            status=True
            if highest_bid_list is None:
                highest_bid_list.append(item.highestbid)
            if decAmount > dechighBid:
                highest_bid_list = extra.uniq(highest_bid_list)
                if highest_bid_list:
                    for bidprice in highest_bid_list:
                        if decimal.Decimal(str(bidprice)) == decAmount: 
                            status=False
                            break

                if status:            
                    bid = Bid(bid_price=amount , user=user_profile, item=item)
                    bid.save()
                    highest_bid_list = extra.uniq(highest_bid_list)
                    if highest_bid_list:
                        item.highestbid = highest_bid_list[0]
                    item.save()
                    #send email to bidderin
                    item_name = bid.item.name
                    owner_email = bid.item.owner.email
                    recipientlist = list(bidQuerySet.values_list('user__email', flat=True))
                    recipientlist.append(owner_email)


                    t = loader.get_template('registration/makebid.txt')
                    c = Context({
					            'amount': 		amount,
					            'item_name': 	item_name,
					            'admin': 		'Kenneth Odoh',
					            'timestamp':	datetime.datetime.now(),
				            })

                    email_subject = 'A new bid has been made on the auction'
                    core_msg = EmailMessage(subject=email_subject, body=t.render(c), from_email='account@example.com', to=recipientlist)

                    core_msg.send(fail_silently=False)
                    return HttpResponseRedirect(reverse('showCurrentBid', args=(bid.id,)))
			        #render bid less than highest bid to template
        else:
            return render_to_response('errors/makebid.html',
                          context_instance=RequestContext(request))        
    else:
        form = BidForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def auction_create(request, template_name="auction/createauction.html"):
    '''
        This is used to create new items(Auctions). The created items are automatically displayed on the latest item and can be searchable. Email is sent to the person who created the item once the item is created.
    '''
    if request.method == 'POST' and request.user.is_authenticated():
        page_title='Auction Creation form'
        postdata = request.POST.copy()
        form = AuctionForm(postdata, request.FILES)
        if form.is_valid():
            human = True
            name = postdata.get('name','')
            description = postdata.get('description','')
            minimum_price = postdata.get('minimum_price',0.01)
            ownerid = request.user.id
            user_profile = get_object_or_404(CustomUser, pk=ownerid)


            item = Item(name=name, description=description, minimum_price=minimum_price, owner=user_profile, highestbid=minimum_price)
            item.save()

            file_content = ContentFile(request.FILES['image'].read())
            item.image.save(request.FILES['image'].name, file_content, save=False)
            item.save()

            t = loader.get_template('registration/createAuction.txt')
            c = Context({
				'firstname': 		user_profile.first_name,
				'lastname': 		user_profile.last_name,
				'site_name': 		'YAAS Auction Site',
				'admin': 			'Kenneth Odoh',
			})

            email_subject = 'Your have created a new auction'
            send_mail(email_subject, t.render(c), 'account@example.com', [user_profile.email], fail_silently=False) 
            return HttpResponseRedirect(reverse('showCurrentItem', args=(item.id,)))
    else:
        form = AuctionForm()			
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



def auction_update(request, item_id, template_name="auction/updateauction.html"):
    '''
        This is used to update new items(Auctions). The currently updated items are automatically displayed on the latest item and can be searchable. Email is sent to the person who updated the item once the item is created. The item can only be updated by the creator of the item. The other users won't even see the link to update an item that they have not created.
    '''
    itemid = item_id
    item = get_object_or_404(Item,  pk=itemid )
    page_title='Auction Update form'
    if request.method == 'POST' and request.user.is_authenticated():
        postdata = request.POST.copy()
        form = AuctionForm(postdata, request.FILES)
        user_profile = get_object_or_404(CustomUser, pk=request.user.id)
        if form.is_valid() and item.owner == user_profile:
            human = True
            name = postdata.get('name','')
            description = postdata.get('description','')
            minimum_price = postdata.get('minimum_price',0.01)
            image = request.FILES['image']

            my_list = []
            if item:
				#update
                if name <> '':
                    item.name = name
                    my_list.append("name")

                if description <> '':
                    item.description = description
                    my_list.append("description")

                if minimum_price <> 0.01:
                    item.minimum_price = minimum_price
                    my_list.append("minimum price")

                if image:
                    file_content = ContentFile(request.FILES['image'].read())
                    item.image.save(request.FILES['image'].name, file_content, save=False)
                    item.save()
                    my_list.append("image")

            item.save()

            t = loader.get_template('registration/updateAuction.txt')
            c = Context({
				'firstname': 		user_profile.first_name,
				'lastname': 		user_profile.last_name,
				'site_name': 		'YAAS Auction Site',
				'admin': 			'Kenneth Odoh',
				'my_list':		    my_list,
			})

            email_subject = 'Your have updated your auction'
            send_mail(email_subject, t.render(c), 'account@example.com', [item.owner.email], fail_silently=False) 
            return HttpResponseRedirect(reverse('showCurrentUpdatedItem', args=(item.id,)))
    else:
        form = AuctionForm()			
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def showAllCreatedAuction(request, template_name="auction/showauction.html"):
    '''
        This is used to display all the created auctions.
    '''
    page_title='Display all auctions'
    myItem = Item.active.filter(owner=request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def showAllMadeBid(request, template_name="auction/showbid.html"):
    '''
        This is used to display all the bids.
    '''
    page_title='Show my created item'
    myBid = Bid.active.filter(user=request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def showCurrentBid(request, bid_id, template_name="auction/showNewbid.html"):
    '''
        This is used to display currently made bid.
    '''
    page_title='Show currently created item'
    newBid = get_object_or_404(Bid, pk=bid_id, user=request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def showCurrentItem(request, item_id, template_name="auction/showNewCreatedItem.html"):
    '''
        This is used to display currently created item.
    '''
    newItem = get_object_or_404(Item, pk=item_id, owner=request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def showCurrentUpdatedBid(request, bid_id, template_name="auction/showupdatedbid.html"):
    '''
        This is used to display currently updated bid.
    '''
    page_title='Show currently updated bid'
    updatedBid = get_object_or_404(Bid, pk=bid_id, user=request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def showCurrentUpdatedItem(request, item_id, template_name="auction/showupdatedItem.html"):
    '''
        This is used to display currently updated item.
    '''
    page_title='Show currently updated item'
    updatedItem = get_object_or_404(Item, pk=item_id, owner=request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required(login_url='/account/login/')
def my_account(request, template_name="account/my_account.html"):
    '''
        This is used to create user profile.
    '''
    page_title='Account Page'
    name = request.user.username
    advertItems = Advertisement.active.all()
    items = Item.active.all()
    num_of_item=items.count()
    item_id = None
    recommendedItem = {}
    mostbiddeditem = None
    result = {}
    itemobjDict = {}
    try: 
        featureditems = Item.active.all()[:5]
        if num_of_item > 10:
            for item in items:
                bids = Bid.active.filter(item = item)
                bidcount = bids.count()
                result[item.id] = bidcount  

            item_id , bidcount = extra.maxValueBid(result)
            mostbiddeditem = get_object_or_404(Item, pk=item_id)
            recommendedItem = extra.sortedItemDictionary(result)
            for key, value in recommendedItem:
                itemObj = get_object_or_404(Item, pk=key)
                itemobjDict[itemObj] = value
    except ValueError:
        pass
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def getBidsOnItem(request, itemid, template_name="auction/bidsfromitem.html"):
    '''
        This is used to get bids from the item.
    '''
    page_title='Bids on item information'
    bids = Bid.active.filter(item__id=itemid)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def getItemDetails(request, item_id, template_name="auction/itemdetails.html"):
    '''
        This is used to item details.
    '''
    page_title="Item's Details"
    userid = request.user.id
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def getPicture(request, item_id, template_name="auction/itempictures.html"):
    '''
        This is used to get pictures of item.
    '''
    page_title='Pictures Details'
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def indexView(request, template_name="index.html"): 
    '''
        This is used to create the index page.
    '''
    page_title='Index Page'
    latestItem = Item.active.all()[:5]
    advertItems = Advertisement.active.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

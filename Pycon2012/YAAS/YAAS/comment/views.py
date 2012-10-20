from YAAS.comment.models import Message
from YAAS.models import Item, CustomUser
from YAAS.comment.forms import MessageForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import get_object_or_404

def base(request, item_id, template_name="comment/base.html"):
    '''
		This displays the comment form.
    '''
    page_title='Comment Form'
    itemid=item_id
    if request.method == 'POST' and request.user.is_authenticated() :
        postdata = request.POST.copy()
        form = MessageForm(postdata)
        if form.is_valid():
            human = True
            text = postdata.get('text','')
            item = get_object_or_404(Item, pk=itemid)
            user = get_object_or_404(CustomUser, pk=request.user.id)
            m = Message(text=text, user=user, item=item)
            m.save()
            url='/comment/{0}/'.format(itemid)
            return HttpResponseRedirect(url)     
    else:
		form = MessageForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def messages(request,item_id, template_name="comment/messages.html"):
    '''
		This displays all the messages.
    '''
    page_title='Display Messages'
    itemid=item_id
    item = get_object_or_404(Item, pk=itemid)
    messages = Message.objects.filter(item=item)[:15]
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

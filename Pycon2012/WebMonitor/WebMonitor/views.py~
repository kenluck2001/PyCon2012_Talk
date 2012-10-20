from django.template import RequestContext, Context,  loader, Template
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from WebMonitor.models import Monitor

def indexView(request, template_name="index.html"): 
    '''
        This is used to create the index page.
    '''
    page_title='Website for Log Statistics'
    monitoredObjList = Monitor.objects.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

from django.template import RequestContext, Context
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from YAAS.advert.models import Advertisement
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from YAAS.advert.forms import AdvertisementForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def advert_create(request, template_name="adverts/advertForm.html"):
    '''
		This creates an advertisement
    '''
    page_title='Advertisement Creation Form'
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = AdvertisementForm(postdata, request.FILES)
        if form.is_valid():
            name = postdata.get('name','')
            description = postdata.get('description','')

            advert = Advertisement(name=name, description=description)
            advert.save()

            file_content = ContentFile(request.FILES['image'].read())
            advert.image.save(request.FILES['image'].name, file_content, save=False)
            advert.save()

            return HttpResponseRedirect(reverse('YAAS.advert.views.getAdvertDetails', args=(advert.id,)))
    else:
        form = AdvertisementForm()			
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))




def showAllAdverts(request, template_name="adverts/showadverts.html"):
    '''
		This displays all the advertisements.
    '''
    page_title='Display all Advertisement'
    advertItems = Advertisement.active.all()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@staff_member_required
def getAdvertDetails(request, advert_id, template_name="adverts/advertdetails.html"):
    '''
		This gets the advertisement's detail.
    '''
    page_title="Advertisement Detail's"
    newAdvert = get_object_or_404(Advertisement, pk=advert_id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

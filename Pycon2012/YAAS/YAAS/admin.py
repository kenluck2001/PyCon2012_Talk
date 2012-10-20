from django.contrib import admin
from YAAS.models import CustomUser, Item, Bid

#This allows CustomUser to be hooked in the admin
admin.site.register(CustomUser)

#This allows Item to be hooked in the admin
admin.site.register(Item)  

#This allows Bid to be hooked in the admin
admin.site.register(Bid)   
    

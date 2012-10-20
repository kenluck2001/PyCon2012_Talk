from django.contrib import admin
from YAAS.comment.models import Message

#attaches Messages model to admin interface
admin.site.register(Message)   

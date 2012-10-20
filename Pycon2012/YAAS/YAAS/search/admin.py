from django.contrib import admin
from YAAS.search.models import SearchTerm

#register searchterm to admin interface
admin.site.register(SearchTerm)   

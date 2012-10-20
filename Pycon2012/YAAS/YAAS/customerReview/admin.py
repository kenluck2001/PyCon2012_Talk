from django.contrib import admin
from YAAS.customerReview.models import ProductReview

#attach ProductReview model to admin interface
admin.site.register(ProductReview)  
 




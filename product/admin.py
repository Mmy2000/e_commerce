from django.contrib import admin
from . models import Product , ProductCategory , ProductImages ,  Color , Size 

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImages)

admin.site.register(Color)
admin.site.register(Size)




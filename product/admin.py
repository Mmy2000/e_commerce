from django.contrib import admin
from . models import Product , ProductCategory , ProductImages ,  Color , Size ,Cart,CartItem,Order,OrderItem

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImages)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Color)
admin.site.register(Size)




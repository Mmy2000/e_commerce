from django.contrib import admin
from .models import Cart , CartItem , Coupon

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code' , 'valid_from' , 'valid_to' , 'discount' , 'active' )
    list_editable = ('active',)
    search_fields = ['code']
admin.site.register(Coupon, CouponAdmin)
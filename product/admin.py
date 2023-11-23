from django.contrib import admin
from . models import Product , ProductCategory , ProductImages ,  Color , Size , ProductReview ,Variation

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImages)

admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductReview)


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Variation,VariationAdmin)





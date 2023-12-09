from django.contrib import admin
from . models import Product , ProductCategory , ProductImages , Variation,ReviewRating , Subcategory
import admin_thumbnails

# Register your models here.
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category')



admin.site.register(ProductCategory)
admin.site.register(Subcategory,SubCategoryAdmin)
admin.site.register(ProductImages)

@admin_thumbnails.thumbnail('image')
class ProductGallaryInline(admin.TabularInline):
    model = ProductImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'price' ,'category' , 'subcategory' , 'stock' , 'created_at' , 'is_available')
    inlines = [ProductGallaryInline]

admin.site.register(Product,ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product' , 'variation_category' , 'variation_value' , 'created_at' , 'is_active' )
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')

admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)





from .models import Info 
from product.models import ProductCategory
from django.db.models import Count


def myfooter(request):
    myfooter = Info.objects.last()
    categories = ProductCategory.objects.all().annotate(product_count=Count('product_category'))[:6]
    context ={
        'myfooter':myfooter,
        'categories':categories,
        }
    return(context)
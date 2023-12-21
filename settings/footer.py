from .models import Info , Brand
from product.models import ProductCategory ,Product,Subcategory
from accounts.models import Profile
from django.db.models import Count
from django.db.models.query_utils import Q
from django.shortcuts import render
from .models import NewsLitter
from django.http import JsonResponse



def myfooter(request):
    myfooter = Info.objects.last()
    categories_footer = ProductCategory.objects.all()
    subcategories = Subcategory.objects.annotate(product_count=Count('product'))    
    brands_footer = Brand.objects.all().annotate(product_count=Count('product_brand'))[:6]
    #profile=Profile.objects.get(user=request.user.id)
    context ={
        'myfooter':myfooter,
        'categories_footer':categories_footer,
        'brands_footer':brands_footer,
        'subcategories':subcategories,
        }
    return(context)

def news_letters_subscribe(request):
    email = request.POST.get('emailinput')
    NewsLitter.objects.create(email=email)
    return JsonResponse({'done':'done'})


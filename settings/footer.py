from .models import Info , Brand
from product.models import ProductCategory ,Product
from django.db.models import Count
from django.db.models.query_utils import Q
from django.shortcuts import render




def myfooter(request):
    myfooter = Info.objects.last()
    categories_footer = ProductCategory.objects.all().annotate(product_count=Count('product_category'))[:6]
    brands_footer = Brand.objects.all().annotate(product_count=Count('product_brand'))[:6]
    context ={
        'myfooter':myfooter,
        'categories_footer':categories_footer,
        'brands_footer':brands_footer,
        }
    return(context)

def home_search(request):
    name = request.GET.get('q','')

    product_list = Product.objects.filter(
        Q(name__icontains = name) |
        Q(description__icontains = name)
    )
    return render(request , 'product/home_search.html' , {'product_list':product_list})
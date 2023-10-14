from .models import Info 
from product.models import ProductCategory ,Product
from django.db.models import Count
from django.shortcuts import render
from django.db.models.query_utils import Q


def myfooter(request):
    myfooter = Info.objects.last()
    categories_footer = ProductCategory.objects.all().annotate(product_count=Count('product_category'))[:6]
    context ={
        'myfooter':myfooter,
        'categories_footer':categories_footer,
        }
    return(context)

def home_search(request):
    name = request.GET.get('name')

    product_list = Product.objects.filter(
        Q(name__icontains = name)
    )
    return render(request , 'settings/home_search.html' , {'product_list':product_list})
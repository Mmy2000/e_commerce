from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import ProductCategory , Product 
from django.shortcuts import render
from django.db.models.query_utils import Q
from django.db.models import Count
from .models import  NewsLitter , Brand , Info
from django.http import JsonResponse

# Create your views here.
def home(request):
    categories_home = ProductCategory.objects.filter().annotate(product_count=Count('product_category'))[:6] 
    product = Product.objects.all()[:8]
    product_just_arrived = Product.objects.all().order_by('-created_at')[:8]

    return render(request, 'settings/home.html',{
        'categories_home':categories_home,
        'product':product ,
        'product_just_arrived':product_just_arrived,
    })

def home_search(request):
    name = request.GET.get('name')

    product_list = Product.objects.filter(
        Q(name__icontains = name) 
    )
    return render(request , 'product/home_search.html' , {'product_list':product_list})


class CategoryList(ListView):
    model = ProductCategory

class BrandList(ListView):
    model = Brand

def news_letters_subscribe(request):
    email = request.POST.get('emailinput')
    NewsLitter.objects.create(email=email)
    return JsonResponse({'done':'done'})


def contact(request):
    site_info = Info.objects.last()
    return render(request,'settings/contact.html',{'site_info': site_info})

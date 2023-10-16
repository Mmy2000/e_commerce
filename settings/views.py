from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import ProductCategory , Product 
from django.shortcuts import render
from django.db.models.query_utils import Q
from django.db.models import Count
from .models import  NewsLitter , Brand
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


class CategoryList(ListView):
    model = ProductCategory

class BrandList(ListView):
    model = Brand

def news_letters_subscribe(request):
    email = request.POST.get('emailinput')
    NewsLitter.objects.create(email=email)
    return JsonResponse({'done':'done'})
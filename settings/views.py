from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import ProductCategory , Product
from django.shortcuts import render
from django.db.models.query_utils import Q
from django.db.models import Count



# Create your views here.
def home(request):
    categories_home = ProductCategory.objects.all().annotate(product_count=Count('product_category'))[:6]
    return render(request, 'settings/home.html',{
        'categories_home':categories_home,
    })


class CategoryList(ListView):
    model = ProductCategory


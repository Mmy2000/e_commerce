from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import ListView , DetailView
from .models import Product
from .models import  ProductCategory , Color, Size 
from django.db.models import Count
from django_filters.views import FilterView
from . filters import ProductFilter
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from accounts.models import Profile
from django.http import JsonResponse
from django.conf import settings
from .forms import ProductReviewForm
from django.views.generic.edit import FormMixin


# Create your views here.

class ProductList(ListView):
    model = Product
    paginate_by = 9


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all().annotate(product_count=Count('product_category'))
        context["sizes"] = Size.objects.all().annotate(product_count=Count('product_size'))
        context["colors"] = Color.objects.all().annotate(product_count=Count('product_color'))

        return context
    
    def get_queryset(self) :
        name = self.request.GET.get('q','')
        object_list = Product.objects.filter(
            Q(name__icontains = name) |
            Q(description__icontains = name)
        )
        return object_list

def like_or_unlike(request,id):
    product = Product.objects.get(id=id)

    if request.user in product.like.all():
        product.like.remove(request.user.id)
    
    else:
        product.like.add(request.user.id)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class Search(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/home_search.html'
    def get_queryset(self) :
        q = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains = q) |
            Q(description__icontains = q))        
        return object_list


class ProductByCategory(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(category__name__icontains = slug)
        )
        return object_list
    
class ProductByBrand(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(PRDBrand__BRDName__icontains = slug)
        )
        return object_list
    
class ProductByTags(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(tags__name__icontains = slug)
        )
        return object_list

class ProductByColor(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(color__name__icontains = slug)
        )
        return object_list
class ProductBysize(ListView):
    model = Product
    paginate_by = 12
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(size__name__icontains = slug)
        )
        return object_list
    

class ProductDetail(FormMixin , DetailView):
    model = Product
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Product.objects.filter(PRDBrand=self.get_object().PRDBrand)
        return context
    
    def post(self , request , *args , **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.product= self.get_object()
            myform.auther = request.user
            myform.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
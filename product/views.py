from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Product
from .models import  ProductCategory , Color, Size
from django.db.models import Count
from django_filters.views import FilterView
from . filters import ProductFilter
from django.db.models.query_utils import Q



# Create your views here.

class ProductList(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all().annotate(product_count=Count('product_category'))
        context["sizes"] = Size.objects.all().annotate(product_count=Count('product_size'))
        context["colors"] = Color.objects.all().annotate(product_count=Count('product_color'))

        return context


class ProductByCategory(ListView):
    model = Product

    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(category__name__icontains = slug)
        )
        return object_list

class ProductByColor(ListView):
    model = Product

    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(color__name__icontains = slug)
        )
        return object_list
class ProductBysize(ListView):
    model = Product

    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(size__name__icontains = slug)
        )
        return object_list

class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Product.objects.filter(category=self.get_object().category)
        return context
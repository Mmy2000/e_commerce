from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import ProductCategory


# Create your views here.
def home(request):
    return render(request, 'settings/home.html',{})


class CategoryList(ListView):
    model = ProductCategory
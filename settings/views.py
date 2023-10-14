from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import ProductCategory , Product
from django.shortcuts import render
from django.db.models.query_utils import Q


# Create your views here.
def home(request):
    return render(request, 'settings/home.html',{})


class CategoryList(ListView):
    model = ProductCategory


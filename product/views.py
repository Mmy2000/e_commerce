from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import ListView , DetailView
from .models import Product , ReviewRating
from .models import  ProductCategory 
from django.db.models import Count
from django_filters.views import FilterView
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from accounts.models import Profile
from django.http import JsonResponse
from django.conf import settings
from django.views.generic.edit import FormMixin
from carts.models import Cart,CartItem
from carts.views import _cart_id
from settings.models import Brand
from django.contrib import messages
from .forms import ReviewForm
from orders.models import OrderProduct
from django_filters.views import FilterView





# Create your views here.

class ProductList(ListView):
    model = Product
    paginate_by = 9


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()

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
        id = self.kwargs['id']
        object_list = Product.objects.filter(
            Q(subcategory__id__icontains = id)
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

    
def product_by_price(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all().annotate(product_count=Count('product_category'))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
            products = products.filter(price__gte=min_price)

    if max_price:
            products = products.filter(price__lte=max_price)
    context = {'products':products,
               'categories':categories}

    return render(request,'product/product_by_price.html',context)

def product_by_variation(request):
    products = Product.objects.all()
    variation_name = request.GET.get('variation_name')
    if variation_name:
        products = products.filter(variation__variation_value__icontains=variation_name)
    context = {'products':products}
    return render(request , 'product/product_by_price.html',context)

def product_detail(request,product_slug):
    try :
        single_product = Product.objects.get(slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        related = Product.objects.filter(PRDBrand=single_product.PRDBrand)
        reviews = ReviewRating.objects.filter(product_id=single_product.id , status=True)
        if request.user.is_authenticated:
            try:
                orderproduct = OrderProduct.objects.filter(user=request.user , product_id=single_product.id).exists()
            except OrderProduct.DoesNotExist:
                orderproduct = None
        else :
            orderproduct = None
        
        orderproduct_2 =  OrderProduct.objects.filter(  product_id=single_product.id)
        orderproduct_count = orderproduct_2.count()

    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'related':related,
        'reviews':reviews,
        'orderproduct':orderproduct,
        'orderproduct_count':orderproduct_count,
    }
    return render(request,'product/product_detail.html',context)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =="POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id , product__id=product_id)
            form = ReviewForm(request.POST , instance=reviews)
            form.save()
            messages.success(request,'Thank You , Your Review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank You , Your Review has been submitted.')
                return redirect(url)
            

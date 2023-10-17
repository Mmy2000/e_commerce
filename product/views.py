from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Product
from .models import  ProductCategory , Color, Size 
from django.db.models import Count
from django_filters.views import FilterView
from . filters import ProductFilter
from django.db.models.query_utils import Q
from .models import Product, Cart, CartItem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect





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


class ProductByCategory(ListView):
    model = Product
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(category__name__icontains = slug)
        )
        return object_list
    
class ProductByBrand(ListView):
    model = Product
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(PRDBrand__BRDName__icontains = slug)
        )
        return object_list

class ProductByColor(ListView):
    model = Product
    template_name = 'product/home_search.html'


    def get_queryset(self) :
        slug = self.kwargs['slug']
        object_list = Product.objects.filter(
            Q(color__name__icontains = slug)
        )
        return object_list
class ProductBysize(ListView):
    model = Product
    template_name = 'product/home_search.html'


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
        context["related"] = Product.objects.filter(PRDBrand=self.get_object().PRDBrand)
        return context
    

    
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('/product')


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('/product/cart/')


@login_required(login_url='login')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'product/cart.html', {'cart_items': cart_items})


@login_required(login_url='login')
def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('/product/cart/')

@login_required(login_url='login')
def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('/product/cart/')

@login_required(login_url='login')
def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count
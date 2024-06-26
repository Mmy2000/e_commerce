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
from django.db.models import Avg
from django.core.paginator import Paginator
from .filters import ProductFilter




# Create your views here.

class ProductList(FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 9
    template_name = 'product/product_list.html'


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

def product_list_orderd_by_rating(request):
    object_list = Product.objects.all().order_by('-reviewrating')
    paginator = Paginator(object_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'object_list': object_list,
               'page_obj':page_obj}
    return render(request, 'product/product_list.html', context)

def product_list_orderd_by_created(request):
    object_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(object_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'object_list': object_list,
               'page_obj':page_obj}
    return render(request , 'product/product_list.html' , context)
def product_list_orderd_by_papularty(request):
    object_list = Product.objects.all().order_by('-views')
    paginator = Paginator(object_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'object_list': object_list,
               'page_obj':page_obj}
    return render(request , 'product/product_list.html' , context)

def product_list_orderd_by_price(request):
    object_list = Product.objects.all().order_by('price')
    paginator = Paginator(object_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'object_list': object_list,
               'page_obj':page_obj}
    return render(request , 'product/product_list.html' , context)

def product_list_orderd_by_price2(request):
    object_list = Product.objects.all().order_by('-price')
    paginator = Paginator(object_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'object_list': object_list,
               'page_obj':page_obj}
    return render(request , 'product/product_list.html' , context)

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
    
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def search(request):
    if is_ajax(request=request):
        product = request.POST.get('product')
        res = None
        # print(product)
        query = Product.objects.filter(name__icontains=product)
        # print(query)
        if len(query) > 0 and len(product) > 0:
            data = []
            for position in query:
                item = {
                    'id' : position.id,
                    'slug' : position.slug,
                    'name' : position.name,
                    'price' : position.price,
                    'image' : str(position.image.url)
                }
                data.append(item)
            res = data
        else:
            res = 'No Products Found ...'

        return JsonResponse({'data':res})
    return JsonResponse({})


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
    categories = ProductCategory.objects.all().annotate(product_count=Count('product'))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    for product in products:
        if product.discount:
            if min_price:
                product = products.filter(discount__gte=min_price)

            if max_price:
                product = products.filter(discount__lte=max_price)
        else:
            if min_price:
                product = products.filter(price__gte=min_price)

            if max_price:
                product = products.filter(price__lte=max_price)
            
    context = {'products':product,
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
        reviews = ReviewRating.objects.filter(product_id=single_product.id , status=True)
        single_product.views+=1
        single_product.save()
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
    related = Product.objects.filter(subcategory=single_product.subcategory)[:3]

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
            

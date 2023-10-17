from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Product
from .models import  ProductCategory , Color, Size , Cart, CartItem, Order, OrderItem
from django.db.models import Count
from django_filters.views import FilterView
from . filters import ProductFilter
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from accounts.models import Profile
from django.http import JsonResponse
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt





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
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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




@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
        

        
def checkout(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    cart_count = get_cart_count(request)
    email = request.user.email
    full_name = request.user.profile.full_name

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'email':email,
        'full_name': full_name
    }
    return render(request, 'product/checkout.html/', context)


@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()
                user = request.user
                user.cart.cartitem_set.all().delete()
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})
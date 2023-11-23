from django.shortcuts import render,redirect,get_object_or_404
from product.models import Product
from .models import Cart , CartItem
from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request , product_id):
    product = Product.objects.get(id=product_id) #get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
            )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('/cart')

def remove_cart(request , product_id):
    
    product = get_object_or_404(Product,id=product_id)

    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product , cart=cart )
    if cart_item.quantity > 0 :
            cart_item.quantity -= 1
            cart_item.save()
    else:
            cart_item.delete()

    return redirect('/cart')

def remove_cart_item(request , product_id):
    
    product = get_object_or_404(Product,id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product ,cart=cart)
    cart_item.delete()
    
    return redirect('/cart')

def cart(request,total=0 ,quantity=0,cart_items=None ):
    try:
        tax = 0
        grand_total=0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.discount:
                total+=(cart_item.product.discount * cart_item.quantity)
                quantity+=cart_item.quantity
            else:
                total+=(cart_item.product.price * cart_item.quantity)
                quantity+=cart_item.quantity
        tax = (2 * total)/100
        grand_total = total+tax
    except Cart.DoesNotExist:
        pass
    context={
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'carts/cart.html',context)
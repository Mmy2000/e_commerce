from django.shortcuts import render,redirect
from carts.models import CartItem
from .forms import OrderForm

# Create your views here.
def place_order(request):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        
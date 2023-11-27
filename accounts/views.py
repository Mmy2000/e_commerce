from django.shortcuts import render , redirect , get_object_or_404
from .forms import SignupForm , UserForm , ProfileForm
from .models import Profile
from product.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login 
from django.db.models import Count
from orders.models import Order , OrderProduct



def signup(request):
    if request.method == "POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
            usernames = form.cleaned_data['username']
            passwords = form.changed_data["password1"]
            user = authenticate(username=usernames,password=passwords)
            login(request,user)

            return redirect('/account/profile')
            
    else:
        form=SignupForm()

    return render(request,'registration/signup.html',{'form':form})



def profile(request):
    profile=Profile.objects.get(user=request.user)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_orderd=True)
    orders_count = orders.count()

    return render(request,'profile/profile.html',{'profile':profile,
                                                  'orders_count':orders_count,})


def edit_profile(requset):
    profile = Profile.objects.get(user=requset.user)
    if requset.method == "POST":
        user_form = UserForm(requset.POST , instance=requset.user)
        profile_form = ProfileForm(requset.POST,requset.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            myprofile = profile_form.save(commit=False)
            myprofile.user = requset.user
            myprofile.save()
            return redirect('/accounts/profile')
    else:
        user_form = UserForm(instance=requset.user)
        profile_form = ProfileForm(instance=profile)

    return render(requset,'profile/profile_edit.html',{
        'user_form':user_form,
        'profile_form':profile_form
    })


def user_favourites(request):
    user_favourites = Product.objects.filter(like=request.user).annotate(product_count=Count('like'))
    product_count = user_favourites.count()
    return render(request,'profile/user_favourite.html',{'user_favourites':user_favourites,
                                                         'product_count':product_count})

def orders(request):
    orders = Order.objects.filter(user=request.user,is_orderd=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request,'profile/orders.html',context)

def order_detail(request,order_id):
    profile=Profile.objects.get(user=request.user)
    orders = Order.objects.get(order_number=order_id)
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'profile':profile,
        'orders':orders,
        'order_detail':order_detail,
        'subtotal':subtotal,
    }
    return render(request,'profile/order_detail.html',context)

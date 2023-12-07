from django.shortcuts import render , redirect , get_object_or_404
from .forms import SignupForm , UserForm , ProfileForm
from .models import Profile
from product.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login 
from django.db.models import Count
from orders.models import Order , OrderProduct
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib import messages



def signup(request):
    if request.method == "POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
            usernames = form.cleaned_data['username']
            passwords = form.cleaned_data["password1"]
            user = authenticate(username=usernames,password=passwords)
            login(request,user)

            return redirect('/accounts/profile')
            
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

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('registration/password_reset_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect(reverse('accounts:forgotPassword'))
    return render(request, 'registration/password_reset_form.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect(reverse('accounts:resetPassword'))
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect(reverse('accounts:resetPassword'))
    else:
        return render(request, 'registration/resetPassword.html')
    

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

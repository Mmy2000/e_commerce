from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import ProductCategory , Product ,Subcategory
from django.shortcuts import render
from django.db.models.query_utils import Q
from django.db.models import Count
from .models import  NewsLitter , Brand , Info
from django.http import JsonResponse
from . forms import ContactForm
from django.core.mail import send_mail


# Create your views here.
def home(request):
    categories_home = ProductCategory.objects.filter()[:6] 
    subcategories = Subcategory.objects.annotate(product_count=Count('product')) 
    product = Product.objects.all()[:8]
    product_just_arrived = Product.objects.all().order_by('-created_at')[:8]

    return render(request, 'settings/home.html',{
        'categories_home':categories_home,
        'product':product ,
        'product_just_arrived':product_just_arrived,
        'subcategories':subcategories
    })




class CategoryList(ListView):
    model = ProductCategory

class BrandList(ListView):
    model = Brand

def news_letters_subscribe(request):
    email = request.POST.get('emailinput')
    NewsLitter.objects.create(email=email)
    return JsonResponse({'done':'done'})


def contact(request):
    site_info = Info.objects.last()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): 
            form.save()
            subject = "Welcome to PythonGuides Training Course"
            message = "Our team will contact you within 24hrs."
            email_from = settings.EMAIL_HOST_USER
            email = form.cleaned_data['email']
            recipient_list =email
            send_mail(subject, message, email_from, [recipient_list])
            return render(request, 'success.html') 
    form = ContactForm()
    context = {'form': form ,
               'site_info': site_info}
    return render(request,'settings/contact.html',context)

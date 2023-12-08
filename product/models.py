from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import Profile
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models import Avg , Count




class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/')
    stock = models.IntegerField()
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    like = models.ManyToManyField(User , blank=True,related_name='product_favourite')
    created_at = models.DateTimeField( default=timezone.now)
    category = models.ForeignKey('ProductCategory',verbose_name=('category'), on_delete=models.CASCADE ,default='')
    subcategory = models.ForeignKey("Subcategory" , on_delete=models.CASCADE ,default='')
    PRDBrand = models.ForeignKey('settings.Brand' ,related_name='product_brand', on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))
    slug = models.SlugField(null=True,blank=True , unique=True)
    tags = TaggableManager()

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)

    def offer(self):
        offer = 0
        if self.discount > 0:
            offer =int( 100 - (self.discount / self.price * 100))
        return offer
    
    def get_absolute_url(self):
        return reverse("product:product_detail", args=[self.slug])

    def __str__(self):
        return self.name
    
    def avr_review(self):
        reviews = ReviewRating.objects.filter(product=self , status=True).aggregate(average=Avg('rating'))
        avg =0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self , status=True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    variation_category = models.CharField( max_length=200 , choices=variation_category_choice)
    variation_value = models.CharField( max_length=200 )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(  auto_now_add=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages/')

    def __str__(self):
        return str(self.product)
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=60)
    

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategoryimages/',blank=True)

    def __str__(self):
        return self.name
    

class ReviewRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500 , blank=True)
    review = models.TextField(max_length=500 , blank=True)
    rating = models.FloatField()
    ip = models.CharField( max_length=50 , blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.subject
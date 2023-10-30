from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import Profile
from django.contrib.auth.models import User
from taggit.managers import TaggableManager




class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/')
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    like = models.ManyToManyField(User , blank=True,related_name='product_favourite')
    created_at = models.DateTimeField( default=timezone.now)
    category = models.ManyToManyField('ProductCategory',related_name='product_category',verbose_name=('category'),  default="")
    PRDBrand = models.ForeignKey('settings.Brand' ,related_name='product_brand', on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))
    color = models.ForeignKey('Color',related_name='product_color',null=True,blank=True, on_delete=models.CASCADE)
    size = models.ForeignKey('Size',related_name='product_size',null=True,blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True,blank=True , unique=True)
    tags = TaggableManager()

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
    
    def get_avg_rating(self):
        all_reviews = self.review_product.all()
        all_rating = 0
        if len(all_reviews)>0:
            for review in all_reviews:
                all_rating += review.rate
            return round(all_rating/len(all_reviews),2)
        else :
            return '-'

class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages/')

    def __str__(self):
        return str(self.product)
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='categoryimages/')

    def __str__(self):
        return self.name
    
class ProductReview(models.Model):
    auther = models.ForeignKey(User, related_name="review_auther", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="review_product", on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    feedback = models.TextField(max_length=2000)
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return str(self.product)

class Color(models.Model):
    name = models.CharField(max_length=50 )

    def __str__(self):
        return str(self.name)
    
class Size(models.Model):
    name = models.CharField(max_length=50 )

    def __str__(self):
        return str(self.name)
    




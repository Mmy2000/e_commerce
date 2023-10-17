from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import Profile
from django.contrib.auth.models import User



# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/')
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    created_at = models.DateTimeField( default=timezone.now)
    category = models.ManyToManyField('ProductCategory',related_name='product_category',verbose_name=('category'),  default="")
    PRDBrand = models.ForeignKey('settings.Brand' ,related_name='product_brand', on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))
    color = models.ManyToManyField('Color',related_name='product_color',null=True,blank=True)
    size = models.ManyToManyField('Size',related_name='product_size',null=True,blank=True)
    slug = models.SlugField(null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

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
    


class Color(models.Model):
    name = models.CharField(max_length=50 )

    def __str__(self):
        return str(self.name)
    
class Size(models.Model):
    name = models.CharField(max_length=50 )

    def __str__(self):
        return str(self.name)
    

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
User.cart = property(lambda u: Cart.objects.get_or_create(user=u)[0])

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

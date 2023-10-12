from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _


# Create your models here.

Size = (
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
)

Color = (
    ('Black','Black'),
    ('White','White'),
    ('Red','Red'),
    ('Blue','Blue'),
    ('Green','Green'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/')
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    created_at = models.DateTimeField( default=timezone.now)
    category = models.ForeignKey('ProductCategory',related_name='product_category',verbose_name=('category'), blank=True, null=True,on_delete=models.CASCADE)
    PRDBrand = models.ForeignKey('settings.Brand' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))
    #size = models.CharField( choices=Size , max_length=100)
    #color = models.CharField( choices=Color , max_length=100)
    slug = models.SlugField(null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages/')

    def __str__(self):
        return str(self.product)
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=60)
    CATParent = models.ForeignKey('self', limit_choices_to={'CATParent__isnull' :True}, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='categoryimages/')

    def __str__(self):
        return self.name

class Product_Alternative(models.Model):
    PALNProduct = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='main_prodcut' , verbose_name=("Product"))
    PALNAlternatives = models.ManyToManyField(Product , related_name='alternative_products'  , verbose_name=("Alternatives"))
    
    class Meta:
        verbose_name = ("Product Alternative")
        verbose_name_plural = ("Product Alternatives")

    def __str__(self):
        return str(self.PALNProduct)


class Product_Accessories(models.Model):
    PACCProduct = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='mainAccessory_prodcut' , verbose_name=("Product"))
    PACCAlternatives = models.ManyToManyField(Product , related_name='accessories_products' , verbose_name=("Accessories"))
      
    class Meta:
        verbose_name = ("Product Accessory")
        verbose_name_plural = ("Product Accessories")

    def __str__(self):
        return str(self.PACCProduct)
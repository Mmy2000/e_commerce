from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Brand(models.Model):
    BRDName = models.CharField(max_length=40)
    image = models.ImageField(upload_to='product/',blank=True, null=True)
    BRDDesc = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.BRDName
    

    

class Info(models.Model):
    site_name = models.CharField( max_length=50)
    description = models.TextField(max_length=1000)
    phone = models.CharField( max_length=30 , null=True, blank=True)
    email = models.EmailField( max_length=254 , null=True, blank=True)
    address = models.CharField( max_length=50 , null=True, blank=True)
    image = models.ImageField(upload_to='settings/', null=True, blank=True )
    fb_link = models.URLField( max_length=200)
    twitter_link = models.URLField( max_length=200)
    instagram_link = models.URLField( max_length=200)

    def __str__(self):
        return self.site_name
    


class NewsLitter(models.Model):
    email = models.EmailField( max_length=254)
    created_at = models.DateTimeField(default=timezone.now)
    

    class Meta:
        verbose_name = ("NewsLitter")
        verbose_name_plural = ("NewsLitter")

    def __str__(self):
        return self.email
    

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    mode_of_contact = models.CharField('Conatct by', max_length=50)
    question_categories = models.CharField('How can we help you?', max_length=50)
    message = models.TextField(max_length=3000)

    def __str__(self):
        return self.email
    
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.


class Coupons(models.Model):
	code 		= models.CharField(max_length=50,unique=True)
	valid_form  = models.DateTimeField()
	valid_to 	= models.DateTimeField()
	discount 	= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	active 		= models.BooleanField()
	class Meta:
		verbose_name = "Coupons"
		verbose_name_plural = "Couponss"

	def __str__(self):
		return self.code
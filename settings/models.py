from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Brand(models.Model):
    BRDName = models.CharField(max_length=40)
    BRDDesc = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.BRDName
    

class Variant(models.Model):
    VARName = models.CharField(max_length=40)
    VARDesc = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Variant")
        verbose_name_plural = _("Variants")

    def __str__(self):
        return self.VARName
    

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
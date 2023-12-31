from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator , MinValueValidator
from django.utils import timezone

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField( max_length=50 , blank=True)
    date_added = models.DateField( auto_now_add=True)


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    variations = models.ManyToManyField("product.Variation",blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        if self.product.discount:
            return self.product.discount * self.quantity
        else:
            return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
    


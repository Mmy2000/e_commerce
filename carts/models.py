from django.db import models
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField( max_length=50 , blank=True)
    date_added = models.DateField( auto_now_add=True)


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
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
    
from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def validate_token(self, token):
        if len(token) == 100: # or whatever length you need
            return True
        return False
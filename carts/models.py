from django.db import models
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField( max_length=50 , blank=True)
    date_added = models.DateField( auto_now_add=True)


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return str(self.product)
    
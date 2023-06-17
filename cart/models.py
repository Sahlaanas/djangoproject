from django.db import models
from checkout.models import Coupon
from useraccount.models import Account
from store.models import Product, ProductAttribute
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank = True)
    is_paid = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    
                
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True, blank=True)
    variant=models.ForeignKey(ProductAttribute,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null = False, blank=False, default=0)
    
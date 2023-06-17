from django.db import models
from useraccount.models import Account
import string
import random
from datetime import datetime
from store.models import Product,ProductAttribute
from user_profile.models import User_Address

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.PositiveIntegerField(default=100)
    minimum_amount = models.PositiveIntegerField(default=500)
    is_applied = models.BooleanField(default=False)
    
    def __str__(self):
        return self.coupon_code
     # Create your models here.
def generate_order_id():
    """Generate a 14-character order ID"""
    while True:
        letters = string.ascii_uppercase + string.digits
        order_id = ''.join(random.choice(letters) for i in range(9))
        year = str(datetime.now().year)[-2:]
        month = str(datetime.now().month)[-2:]
        day = str(datetime.now().day)
        hour = str(datetime.now().hour)
        new_id = 'LK' + month + day + hour+ order_id
        return new_id
    
class Payment_methods(models.Model):
    method = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.method
        

class Order(models.Model):
    order_id = models.CharField(max_length=20, default=generate_order_id, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    user_address = models.ForeignKey(User_Address, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_mode = models.ForeignKey(Payment_methods, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=250, null=True)
    paid = models.BooleanField(default=False, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    


    
    def __str__(self) -> str:
        return self.order_id




class Order_item(models.Model):
   
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductAttribute,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='photos/order')
    price = models.PositiveIntegerField()
    total=models.PositiveIntegerField()
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    
    

    def get_total(self):
        return self.variant.price * self.quantity
    
    def __str__(self) -> str:
        return str(self.order)






    
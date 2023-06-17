from django.db import models
from useraccount.models import Account
from store.models import Product,ProductAttribute

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    variant = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
from django.db import models
from user_brand.models import Brand
from user_category.models import Category
from django.utils.text import slugify
from django.utils.html import mark_safe

# Create your models here.
class screenSizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.size_name
    
class RAMVariant(models.Model):
    RAM_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.RAM_name
    
# class price_filter(models.Model):
#     filter_price = (
        
#         ('1000 T 10000', '1000 TO 10000'),
#         ('10000 TO 20000', '10000 TO 20000'),
#         ('20000 TO 30000', '20000 TO 30000'),
#         ('30000 TO 40000', '30000 TO 40000'),
#         ('40000 TO 50000', '40000 TO 50000'),
#         ('50000 and above', '50000 and above'),
        
#         )
#     price = models.CharField(choices=filter_price, max_length=60)
    
#     def __str__(self):
#         return self.price
    
    
class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_amount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.offer_name





class Product(models.Model):
    slug = models.SlugField(max_length=100, unique = True)
    product_name = models.CharField(unique=True,max_length=50)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    size = models.ForeignKey(screenSizeVariant, on_delete=models.CASCADE, blank=True, null=True)
    ram = models.ForeignKey(RAMVariant,on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    

    def __str__(self):
        return self.product_name
    
   

class Product_Image(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/product')
   
    def __str__(self) -> str:
        return str(self.product)


class ProductAttribute(models.Model):
      product = models.ForeignKey(Product, on_delete=models.CASCADE)
      size = models.ForeignKey(screenSizeVariant, on_delete=models.CASCADE)
      ram = models.ForeignKey(RAMVariant, on_delete=models.CASCADE)
      price = models.PositiveIntegerField()
      image = models.ImageField(upload_to='photos/product',null=True)
      stock = models.PositiveIntegerField()
      offer = models.ForeignKey(Offer, on_delete=models.CASCADE, blank=True, null=True)
      
      def get_offer(self):
        return self.price - self.offer.discount_amount
      
      def image_tag(self):
          return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
      
      def __str__(self):
            return self.product.product_name
        
        
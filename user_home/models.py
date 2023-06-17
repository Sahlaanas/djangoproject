from django.db import models
from user_category.models import Category

# Create your models here.
# BANNER MODEL
class Banner(models.Model):
    banner_image = models.ImageField(upload_to='photos/banner')
    banner_name = models.CharField(max_length=200)
    banner_description = models.TextField(max_length=300)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    offer = models.CharField(max_length=200, default = None, null=True)
    
    def __str__(self):
        return self.banner_name
    
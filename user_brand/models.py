from django.db import models
from django.utils.text import slugify


# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique = True)
    brand_image = models.ImageField(upload_to='photos/brand', default = 'No image available')
    brand_address = models.TextField(max_length=200)
    brand_description = models.TextField(max_length=300) 
    
    
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.brand_name
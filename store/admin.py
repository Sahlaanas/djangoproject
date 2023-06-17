from django.contrib import admin
from .models import Product,Product_Image,screenSizeVariant,RAMVariant, ProductAttribute,Offer

# Register your models here.
class Product_ImageAdmin(admin.StackedInline):
    model = Product_Image
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [Product_ImageAdmin]
    prepopulated_fields = {'slug' : ('product_name',)}
    
admin.site.register(Product_Image)
admin.site.register(Product, ProductAdmin)

@admin.register(screenSizeVariant)
class screenSizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price', 'stock']
    model = screenSizeVariant
    
  
@admin.register(RAMVariant)    
class RAMVariantAdmin(admin.ModelAdmin):
    list_display = ['RAM_name', 'price', 'stock']
    model = RAMVariant
    
    
class ProductAttributeAdmin(admin.ModelAdmin):
      list_display = ('product', 'price', 'size', 'ram', 'image_tag')
      
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Offer)
from django.contrib import admin
from .models import Coupon,Order,Order_item,Payment_methods
 

# Register your models here.
admin.site.register(Coupon)
class OrderItemTableInline(admin.TabularInline):
    model=Order_item
    
class OrderAdmin(admin.ModelAdmin):
    inlines= [OrderItemTableInline]
    
admin.site.register(Order,OrderAdmin)

admin.site.register(Payment_methods)
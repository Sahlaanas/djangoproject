from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('delete-from-cart/',views.deleteCartItem, name='delete-from-cart'),
    path('update-cart/', views.updateCartItem, name="update-cart")
    
 
   
]

from django.urls import path
from . import views






urlpatterns = [
    path('', views.wishlist, name = 'wishlist'),
    path('add-to-wishlist/', views.addTowishlist, name = 'addTowishlist'),
    path('deleteWishlistItem/', views.remove_wishlist, name = 'remove_wishlist'),
    
   
  
]